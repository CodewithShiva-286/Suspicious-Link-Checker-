from app.config.settings import get_settings
from app.decision_engine.models import SignalResult
from app.decision_engine.scoring import evaluate_signals


def test_malicious_override_from_google():
    settings = get_settings()
    signals = [
        SignalResult(
            source="google_safe_browsing",
            status="malicious",
            score=95,
            confidence=95,
            details="Threat found.",
            raw_ref="x",
            latency_ms=100,
            error=None,
        ),
        SignalResult(
            source="virustotal",
            status="safe",
            score=10,
            confidence=90,
            details="No detections.",
            raw_ref="y",
            latency_ms=100,
            error=None,
        ),
    ]
    decision = evaluate_signals(signals, settings)
    assert decision.verdict == "malicious"
