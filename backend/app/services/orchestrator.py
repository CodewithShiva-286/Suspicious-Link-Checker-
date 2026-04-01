import asyncio
from datetime import datetime

from app.config.settings import Settings
from app.decision_engine.models import SignalResult
from app.services.normalizer import normalize_provider_result
from app.services.providers.google_safe_browsing import check_google_safe_browsing
from app.services.providers.ssl_check import check_ssl
from app.services.providers.virustotal import check_virustotal
from app.services.providers.whois_lookup import check_whois
from app.utils.time_utils import utc_now


def _event(event: str, source: str, status: str, message: str, ts: datetime | None = None) -> dict:
    return {
        "event": event,
        "source": source,
        "status": status,
        "message": message,
        "timestamp": ts or utc_now(),
    }


async def run_scan(url: str, domain: str, settings: Settings) -> tuple[list[SignalResult], list[dict]]:
    timeline: list[dict] = [_event("URL_RECEIVED", "system", "ok", "URL received for scanning.")]
    timeline.extend(
        [
            _event("GOOGLE_CHECK_STARTED", "google_safe_browsing", "running", "Starting Google Safe Browsing check."),
            _event("VT_CHECK_STARTED", "virustotal", "running", "Starting VirusTotal check."),
            _event("WHOIS_CHECK_STARTED", "whois", "running", "Starting WHOIS lookup."),
            _event("SSL_CHECK_STARTED", "ssl", "running", "Starting SSL inspection."),
        ]
    )

    tasks = [
        check_google_safe_browsing(url, settings),
        check_virustotal(url, settings),
        check_whois(domain),
        check_ssl(domain),
    ]
    raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    signals: list[SignalResult] = []
    for item in raw_results:
        if isinstance(item, Exception):
            signals.append(
                normalize_provider_result(
                    {
                        "source": "unknown",
                        "status": "unknown",
                        "score": 50,
                        "confidence": 10,
                        "details": "Provider execution failed.",
                        "error": str(item),
                    }
                )
            )
            continue
        signal = normalize_provider_result(item)
        signals.append(signal)
        timeline.append(
            _event(
                f"{signal.source.upper()}_CHECK_COMPLETED",
                signal.source,
                signal.status,
                signal.details,
            )
        )

    timeline.append(_event("DECISION_ENGINE_STARTED", "decision_engine", "running", "Evaluating normalized signals."))
    return signals, timeline
