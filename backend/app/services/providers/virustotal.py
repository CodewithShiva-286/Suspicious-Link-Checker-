import asyncio
import logging
from datetime import datetime

import httpx

from app.config.settings import Settings
from app.utils.time_utils import elapsed_ms, utc_now

logger = logging.getLogger(__name__)

VT_ANALYSIS_MAX_RETRIES = 5
VT_ANALYSIS_POLL_DELAY_S = 2.0


async def _poll_analysis_until_complete(
    client: httpx.AsyncClient,
    analysis_endpoint: str,
    headers: dict[str, str],
    analysis_id: str,
) -> tuple[dict | None, str | None]:
    """Poll GET /analyses/{id} until completed, or return reason: timeout | failed."""
    for attempt in range(1, VT_ANALYSIS_MAX_RETRIES + 1):
        analysis_response = await client.get(analysis_endpoint, headers=headers)
        _raise_with_rate_limit_context(analysis_response)
        payload = analysis_response.json()
        status = payload.get("data", {}).get("attributes", {}).get("status")
        logger.info(
            "VirusTotal analysis poll: id=%s attempt=%s/%s status=%s",
            analysis_id,
            attempt,
            VT_ANALYSIS_MAX_RETRIES,
            status,
        )
        if status == "completed":
            return payload, None
        if status == "failed":
            logger.warning(
                "VirusTotal analysis failed: id=%s attempt=%s",
                analysis_id,
                attempt,
            )
            return None, "failed"
        if attempt < VT_ANALYSIS_MAX_RETRIES:
            await asyncio.sleep(VT_ANALYSIS_POLL_DELAY_S)
    logger.warning(
        "VirusTotal analysis not completed after %s polls: id=%s",
        VT_ANALYSIS_MAX_RETRIES,
        analysis_id,
    )
    return None, "timeout"


async def check_virustotal(url: str, settings: Settings) -> dict:
    start = utc_now()
    if not settings.VIRUSTOTAL_API_KEY:
        return _unknown("Missing API key", start)

    submit_endpoint = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}

    try:
        timeout = settings.REQUEST_TIMEOUT_MS / 1000
        async with httpx.AsyncClient(timeout=timeout) as client:
            submit_response = await client.post(
                submit_endpoint,
                headers=headers,
                data={"url": url},
            )
            _raise_with_rate_limit_context(submit_response)
            submit_data = submit_response.json()

            analysis_id = submit_data.get("data", {}).get("id")
            if not analysis_id:
                return _unknown("VirusTotal submit response did not include analysis id.", start)

            analysis_endpoint = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            analysis_data, poll_reason = await _poll_analysis_until_complete(
                client, analysis_endpoint, headers, analysis_id
            )
            if analysis_data is None:
                if poll_reason == "failed":
                    return _unknown(
                        "VirusTotal analysis failed.",
                        start,
                        details="VirusTotal analysis failed.",
                    )
                return _unknown(
                    "Analysis not completed in time",
                    start,
                    details="Analysis not completed in time",
                )
    except httpx.HTTPStatusError as exc:
        return _unknown(_format_http_error(exc), start)
    except Exception as exc:
        return _unknown(str(exc), start)

    attrs = analysis_data.get("data", {}).get("attributes", {})
    stats = attrs.get("stats", {})
    malicious = int(stats.get("malicious", 0))
    suspicious = int(stats.get("suspicious", 0))
    harmless = int(stats.get("harmless", 0))
    undetected = int(stats.get("undetected", 0))
    total = max(1, malicious + suspicious + harmless + undetected)

    if malicious >= 5:
        status, score, confidence = "malicious", 85, 90
    elif malicious > 0 or suspicious > 0:
        ratio = (malicious + suspicious) / total
        status, score, confidence = "suspicious", min(75, round(30 + ratio * 100)), 75
    else:
        status, score, confidence = "safe", 10, 85

    return {
        "source": "virustotal",
        "status": status,
        "score": score,
        "confidence": confidence,
        "details": (
            "VirusTotal analysis stats: "
            f"malicious={malicious}, suspicious={suspicious}, harmless={harmless}, undetected={undetected}."
        ),
        "raw_ref": "vt.analysis.stats",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": None,
    }


def _raise_with_rate_limit_context(response: httpx.Response) -> None:
    if response.status_code == 429:
        raise httpx.HTTPStatusError(
            "VirusTotal rate limit exceeded (429).",
            request=response.request,
            response=response,
        )
    response.raise_for_status()


def _format_http_error(exc: httpx.HTTPStatusError) -> str:
    status = exc.response.status_code if exc.response is not None else "unknown"
    if status == 429:
        return "VirusTotal rate limit exceeded (429)."
    return f"VirusTotal HTTP error {status}: {exc}"


def _unknown(error: str, start: datetime, details: str | None = None) -> dict:
    return {
        "source": "virustotal",
        "status": "unknown",
        "score": 50,
        "confidence": 25,
        "details": details or "VirusTotal check unavailable.",
        "raw_ref": "vt.error",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": error,
    }
