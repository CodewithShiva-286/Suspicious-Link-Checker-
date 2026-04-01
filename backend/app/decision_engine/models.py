from pydantic import BaseModel, Field


class SignalResult(BaseModel):
    source: str
    status: str
    score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    details: str
    raw_ref: str | None = None
    latency_ms: int = Field(default=0, ge=0)
    error: str | None = None


class DecisionOutput(BaseModel):
    verdict: str
    risk_score: int = Field(ge=0, le=100)
    confidence_score: int = Field(ge=0, le=100)
    reasons: list[str]
    rule_trace: list[str]
