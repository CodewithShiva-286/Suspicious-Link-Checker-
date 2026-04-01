from app.decision_engine.models import SignalResult


def normalize_provider_result(result: dict) -> SignalResult:
    return SignalResult(
        source=result.get("source", "unknown"),
        status=result.get("status", "unknown"),
        score=int(result.get("score", 50)),
        confidence=int(result.get("confidence", 25)),
        details=result.get("details", "No details available."),
        raw_ref=result.get("raw_ref"),
        latency_ms=int(result.get("latency_ms", 0)),
        error=result.get("error"),
    )
