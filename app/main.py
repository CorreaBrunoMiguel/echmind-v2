from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.config import settings
from app.core.telemetry import setup_tracing
from app.core.correlation import CorrelationIdMiddleware
from app.api.v1.routers.status import router as status_router
from app.api.v1.routers.dev_stub import dev_stub_router

app = FastAPI(title=settings.app_name, version=settings.version)
app.add_middleware(CorrelationIdMiddleware, api_version=settings.version)

setup_tracing(settings.app_name, settings.version, settings.otlp_endpoint)
FastAPIInstrumentor().instrument_app(app)

app.include_router(status_router)
app.include_router(dev_stub_router)