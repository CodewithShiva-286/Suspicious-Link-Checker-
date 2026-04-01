from datetime import datetime
from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)


class TimelineEvent(BaseModel):
    event: str
    source: str
    status: str
    message: str
    timestamp: datetime


class ProviderResponse(BaseModel):
    source: str
    status: str
    score: int
    confidence: int
    details: str
    raw_ref: str | None = None
    latency_ms: int
    error: str | None = None


class DecisionResponse(BaseModel):
    verdict: str
    risk_score: int
    confidence_score: int
    reasons: list[str]
    rule_trace: list[str]


class ScanResponse(BaseModel):
    scan_id: str
    input_url: str
    canonical_url: str
    decision: DecisionResponse
    provider_results: list[ProviderResponse]
    timeline_events: list[TimelineEvent]
    started_at: datetime
    completed_at: datetime
    duration_ms: int
