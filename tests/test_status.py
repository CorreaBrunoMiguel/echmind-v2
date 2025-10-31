import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_status_returns_correlation_id_and_headers():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/status")
        assert r.status_code == 200
        body = r.json()
        assert "correlation_id" in body and body["correlation_id"]
        assert r.headers.get("X-Correlation-Id") == body["correlation_id"]
        assert r.headers.get("X-API-Version") is not None

@pytest.mark.asyncio
async def test_health_and_ready():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        assert (await ac.get("/api/v1/healthz")).json()["ok"] is True
        assert (await ac.get("/api/v1/readyz")).json()["ready"] is True
