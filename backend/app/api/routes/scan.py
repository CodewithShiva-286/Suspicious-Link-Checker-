from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.scan import DecisionResponse, ProviderResponse, ScanRequest, ScanResponse, TimelineEvent
from app.config.settings import Settings, get_settings
from app.database.repositories.scan_repository import ScanRepository
from app.decision_engine.scoring import evaluate_signals
from app.services.orchestrator import run_scan
from app.utils.time_utils import elapsed_ms, utc_now
from app.utils.url_utils import UrlValidationError, canonicalize_url

router = APIRouter(prefix="/scan", tags=["scan"])
scan_repo = ScanRepository()


@router.post("", response_model=ScanResponse)
async def create_scan(payload: ScanRequest, settings: Settings = Depends(get_settings)) -> ScanResponse:
    started_at = utc_now()

    try:
        canonical_url, domain = canonicalize_url(payload.url, settings)
    except UrlValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    signals, timeline = await run_scan(canonical_url, domain, settings)
    decision = evaluate_signals(signals, settings)
    timeline.append(
        {
            "event": "DECISION_ENGINE_COMPLETED",
            "source": "decision_engine",
            "status": decision.verdict,
            "message": f"Scan completed with verdict={decision.verdict}.",
            "timestamp": utc_now(),
        }
    )

    scan_id = str(uuid4())
    completed_at = utc_now()
    document = {
        "scan_id": scan_id,
        "input": {"url": payload.url, "canonical_url": canonical_url, "domain": domain},
        "provider_results": [item.model_dump() for item in signals],
        "decision": decision.model_dump(),
        "timeline_events": timeline,
        "meta": {
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_ms": elapsed_ms(started_at, completed_at),
            "status": "completed",
        },
    }
    if settings.ENABLE_SCAN_PERSISTENCE:
        await scan_repo.insert_scan(document)

    return ScanResponse(
        scan_id=scan_id,
        input_url=payload.url,
        canonical_url=canonical_url,
        decision=DecisionResponse(**decision.model_dump()),
        provider_results=[ProviderResponse(**item.model_dump()) for item in signals],
        timeline_events=[TimelineEvent(**event) for event in timeline],
        started_at=started_at,
        completed_at=completed_at,
        duration_ms=elapsed_ms(started_at, completed_at),
    )


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str) -> ScanResponse:
    item = await scan_repo.get_by_scan_id(scan_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return ScanResponse(
        scan_id=item["scan_id"],
        input_url=item["input"]["url"],
        canonical_url=item["input"]["canonical_url"],
        decision=DecisionResponse(**item["decision"]),
        provider_results=[ProviderResponse(**entry) for entry in item["provider_results"]],
        timeline_events=[TimelineEvent(**entry) for entry in item["timeline_events"]],
        started_at=item["meta"]["started_at"],
        completed_at=item["meta"]["completed_at"],
        duration_ms=item["meta"]["duration_ms"],
    )
