from fastapi import APIRouter, Request
router = APIRouter(prefix="/api/v1", tags=["status"])

@router.get("/status")
async def status(request: Request):
    return {
        "service": "echomind-engine",
        "version": request.headers.get("X-API-Version") or "0.2.0",
        "correlation_id": getattr(request.state, "correlation_id", None)
    }
    
@router.get("/healthz")
async def healthz():
    return {"ok": True}

@router.get('/readyz')
async def readyz():
    # futuro: checar DB/OTLP
    return {"ready": True}