from datetime import datetime

import whois

from app.utils.time_utils import elapsed_ms, utc_now


async def check_whois(domain: str) -> dict:
    start = utc_now()
    try:
        result = whois.whois(domain)
    except Exception as exc:
        return _unknown(str(exc), start)

    created = result.creation_date
    if isinstance(created, list) and created:
        created = created[0]

    if not created:
        return {
            "source": "whois",
            "status": "unknown",
            "score": 45,
            "confidence": 35,
            "details": "WHOIS creation date not available.",
            "raw_ref": "whois.missing_creation_date",
            "latency_ms": elapsed_ms(start, utc_now()),
            "error": None,
        }

    age_days = max(0, (utc_now().date() - created.date()).days)
    if age_days < 30:
        status, score, confidence = "suspicious", 70, 80
    elif age_days < 180:
        status, score, confidence = "suspicious", 45, 75
    else:
        status, score, confidence = "safe", 15, 85

    return {
        "source": "whois",
        "status": status,
        "score": score,
        "confidence": confidence,
        "details": f"Domain age is {age_days} days.",
        "raw_ref": "whois.creation_date",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": None,
    }


def _unknown(error: str, start: datetime) -> dict:
    return {
        "source": "whois",
        "status": "unknown",
        "score": 50,
        "confidence": 25,
        "details": "WHOIS lookup unavailable.",
        "raw_ref": "whois.error",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": error,
    }
