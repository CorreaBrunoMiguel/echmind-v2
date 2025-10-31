from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.core.config import settings
from app.core.telemetry import setup_tracing
from app.core.correlation import CorrelationIdMiddleware
from app.api.v1.routers.status import router as status_router
from app.api.v1.routers.dev_stub import router as dev_stub_router
from app.api.errors import http_exception_handler, generic_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

app = FastAPI(title=settings.app_name, version=settings.version)
app.add_middleware(CorrelationIdMiddleware, api_version=settings.version)

setup_tracing(settings.app_name, settings.version, settings.otlp_endpoint)
FastAPIInstrumentor().instrument_app(app)

# routers
app.include_router(status_router)
app.include_router(dev_stub_router)

# handlers de erro
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
# (opcional: tratar validações pydantic como problem+json)
async def validation_handler(request, exc: RequestValidationError):
    return await http_exception_handler(request, HTTPException(status_code=422, detail="Unprocessable Entity"))
app.add_exception_handler(RequestValidationError, validation_handler)
