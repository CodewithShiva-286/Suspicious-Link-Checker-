from app.config.settings import Settings
from app.decision_engine.explainer import to_output
from app.decision_engine.models import DecisionOutput, SignalResult
from app.decision_engine.rules import PROVIDER_WEIGHTS


def _status_override(signals: list[SignalResult], settings: Settings) -> str | None:
    for signal in signals:
        if signal.source == "google_safe_browsing" and signal.status == "malicious":
            return "malicious"
        if signal.source == "virustotal" and signal.status == "malicious":
            if signal.score >= min(settings.VT_MALICIOUS_OVERRIDE_THRESHOLD * 10, 100):
                return "malicious"
    return None


def _bucket_verdict(risk_score: int) -> str:
    if risk_score >= 60:
        return "malicious"
    if risk_score >= 25:
        return "suspicious"
    return "safe"


def evaluate_signals(signals: list[SignalResult], settings: Settings) -> DecisionOutput:
    if not signals:
        return DecisionOutput(
            verdict="suspicious",
            risk_score=50,
            confidence_score=10,
            reasons=["No provider results were available."],
            rule_trace=["no_signals"],
        )

    weighted_sum = 0.0
    total_coverage = 0.0
    confidence_values: list[int] = []
    unknown_count = 0

    for signal in signals:
        weight = PROVIDER_WEIGHTS.get(signal.source, 0.0)
        conf_factor = signal.confidence / 100
        weighted_sum += signal.score * weight * conf_factor
        total_coverage += weight
        confidence_values.append(signal.confidence)
        if signal.status == "unknown":
            unknown_count += 1

    risk_score = max(0, min(100, round(weighted_sum)))
    base_conf = sum(confidence_values) / len(confidence_values)
    coverage_factor = min(1.0, total_coverage)
    conflict_penalty = 10 if _has_conflict(signals) else 0
    unknown_penalty = unknown_count * 12
    confidence_score = round(max(0, min(100, (base_conf * coverage_factor) - conflict_penalty - unknown_penalty)))

    verdict = _status_override(signals, settings) or _bucket_verdict(risk_score)
    if _high_trust_sources_missing(signals):
        verdict = "suspicious" if verdict == "safe" else verdict
        confidence_score = min(confidence_score, 45)

    return to_output(verdict, risk_score, confidence_score, signals)


def _has_conflict(signals: list[SignalResult]) -> bool:
    states = {s.status for s in signals if s.status in {"safe", "suspicious", "malicious"}}
    return "safe" in states and "malicious" in states


def _high_trust_sources_missing(signals: list[SignalResult]) -> bool:
    by_source = {s.source: s for s in signals}
    for source in ("google_safe_browsing", "virustotal"):
        signal = by_source.get(source)
        if signal is None or signal.status == "unknown":
            return True
    return False
