import socket
import ssl
from datetime import datetime

from app.utils.time_utils import elapsed_ms, utc_now


async def check_ssl(hostname: str) -> dict:
    start = utc_now()
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                cert = secure_sock.getpeercert()
    except Exception as exc:
        return _unknown(str(exc), start)

    not_after = cert.get("notAfter")
    if not not_after:
        return {
            "source": "ssl",
            "status": "suspicious",
            "score": 60,
            "confidence": 60,
            "details": "Certificate expiration date unavailable.",
            "raw_ref": "ssl.no_expiry",
            "latency_ms": elapsed_ms(start, utc_now()),
            "error": None,
        }

    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    now_naive = datetime.utcnow()
    if expiry < now_naive:
        status, score, confidence = "malicious", 80, 90
        details = f"SSL certificate expired on {expiry.date()}."
    else:
        remaining_days = (expiry - now_naive).days
        if remaining_days <= 7:
            status, score, confidence = "suspicious", 55, 85
            details = f"SSL certificate expires soon ({remaining_days} days)."
        else:
            status, score, confidence = "safe", 10, 90
            details = f"SSL certificate is valid ({remaining_days} days remaining)."

    return {
        "source": "ssl",
        "status": status,
        "score": score,
        "confidence": confidence,
        "details": details,
        "raw_ref": "ssl.certificate",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": None,
    }


def _unknown(error: str, start: datetime) -> dict:
    return {
        "source": "ssl",
        "status": "unknown",
        "score": 50,
        "confidence": 25,
        "details": "SSL certificate check unavailable.",
        "raw_ref": "ssl.error",
        "latency_ms": elapsed_ms(start, utc_now()),
        "error": error,
    }
