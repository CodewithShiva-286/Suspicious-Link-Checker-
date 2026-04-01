from datetime import datetime

import httpx

from app.config.settings import Settings
from app.utils.time_utils import elapsed_ms, utc_now


async def check_google_safe_browsing(url: str, settings: Settings) -> dict:
    start = utc_now()
    if not settings.GOOGLE_SAFE_BROWSING_API_KEY:
        return _unknown("Missing API key", start)

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={settings.GOOGLE_SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {"clientId": "link_checker", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        timeout = settings.REQUEST_TIMEOUT_MS / 1000
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return _unknown(str(exc), start)

    matches = data.get("matches", [])
    if matches:
        return {
            "source": "google_safe_browsing",
            "status": "malicious",
            "score": 90,
            "confidence": 95,
            "details": "Threat match found in Google Safe Browsing.",
            "raw_ref": "gsb.matches",
            "latency_ms": elapsed_ms(start, utc_now()),
            "error": None,
        }
    return {
        "source": "google_safe_browsing",
        "status": "safe",
        "score": 5,
        "confidence": 90,
        "details": "No threat match found by Google Safe Browsing.",
        "raw_ref": "gsb.no_match",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": None,
    }


def _unknown(error: str, start: datetime) -> dict:
    return {
        "source": "google_safe_browsing",
        "status": "unknown",
        "score": 50,
        "confidence": 25,
        "details": "Google Safe Browsing check unavailable.",
        "raw_ref": "gsb.error",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": error,
    }
