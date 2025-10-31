import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_problem_details_contains_required_fields_and_headers():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/dev/boom")
        assert r.status_code == 400
        assert r.headers.get("content-type").startswith("application/problem+json")
        body = r.json()
        # campos RFC7807
        for key in ["type", "title", "status", "instance", "correlation_id"]:
            assert key in body
        # correlação coerente com header
        assert r.headers.get("X-Correlation-Id") == body.get("correlation_id")
        # versão sempre presente
        assert r.headers.get("X-API-Version")
