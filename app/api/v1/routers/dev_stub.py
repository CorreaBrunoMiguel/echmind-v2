from fastapi import APIRouter, Depends
from app.domain.ports import EchoRepo, TraceRepo, PulseSource, AnchorRepo
from app.api.deps import (
    get_echo_repo, get_trace_repo, get_pulse_source, get_anchor_repo
)

router = APIRouter(prefix="/api/v1/dev", tags=["dev"])

@router.get("/di-check")
async def di_check(
    echo_repo: EchoRepo = Depends(get_echo_repo),
    trace_repo: TraceRepo = Depends(get_trace_repo),
    pulse_source: PulseSource = Depends(get_pulse_source),
    anchor_repo: AnchorRepo = Depends(get_anchor_repo),
):
    # Não chamamos métodos (levantariam NotImplementedError): apenas provamos o DI.
    return {
        "echo_repo": echo_repo.__class__.__name__,
        "trace_repo": trace_repo.__class__.__name__,
        "pulse_source": pulse_source.__class__.__name__,
        "anchor_repo": anchor_repo.__class__.__name__,
    }

dev_stub_router = router
__all__ = ["router", "dev_stub_router"]