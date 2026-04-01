from app.decision_engine.models import DecisionOutput, SignalResult


def build_reason_trace(signals: list[SignalResult], verdict: str) -> tuple[list[str], list[str]]:
    reasons: list[str] = []
    trace: list[str] = []

    for signal in signals:
        state = signal.status.upper()
        trace.append(f"{signal.source}: status={state}, score={signal.score}, confidence={signal.confidence}")
        if signal.error:
            reasons.append(f"{signal.source} check failed: {signal.error}.")
        elif signal.status in {"malicious", "suspicious"}:
            reasons.append(f"{signal.source}: {signal.details}")

    if not reasons:
        reasons.append("No provider flagged clear malicious behavior.")
    trace.append(f"final_verdict={verdict}")
    return reasons, trace


def to_output(
    verdict: str,
    risk_score: int,
    confidence_score: int,
    signals: list[SignalResult],
) -> DecisionOutput:
    reasons, trace = build_reason_trace(signals, verdict)
    return DecisionOutput(
        verdict=verdict,
        risk_score=risk_score,
        confidence_score=confidence_score,
        reasons=reasons,
        rule_trace=trace,
    )
