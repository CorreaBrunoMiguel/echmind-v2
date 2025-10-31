from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from starlette import status as http
from app.api.schemas import Problem

CONTENT_TYPE = "application/problem+json"

def _cid(request: Request) -> str | None:
    return getattr(getattr(request, "state", None), "correlation_id", None)

async def http_exception_handler(request: Request, exc: HTTPException):
    prob = Problem(
        type=f"https://httpstatuses.io/{exc.status_code}",
        title=exc.detail if isinstance(exc.detail, str) else exc.__class__.__name__,
        status=exc.status_code,
        detail=exc.detail if isinstance(exc.detail, str) else None,
        instance=str(request.url.path),
        correlation_id=_cid(request),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=prob.model_dump(),
        media_type=CONTENT_TYPE,
    )

async def generic_exception_handler(request: Request, exc: Exception):
    prob = Problem(
        type="about:blank",
        title="Internal Server Error",
        status=http.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc)[:400],
        instance=str(request.url.path),
        correlation_id=_cid(request),
    )
    return JSONResponse(
        status_code=http.HTTP_500_INTERNAL_SERVER_ERROR,
        content=prob.model_dump(),
        media_type=CONTENT_TYPE,
    )
