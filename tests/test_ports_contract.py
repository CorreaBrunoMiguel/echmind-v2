import pytest
from httpx import AsyncClient

from app.domain import ports
from app.adapters.stubs.echo_repo import StubEchoRepo
from app.adapters.stubs.trace_repo import StubTraceRepo
from app.adapters.stubs.pulse_source import StubPulseSource
from app.adapters.stubs.anchor_repo import StubAnchorRepo
from app.main import app

@pytest.mark.asyncio
async def test_ports_exist_and_have_expected_attributes():
    assert hasattr(ports, "EchoRepo")
    assert hasattr(ports, "TraceRepo")
    assert hasattr(ports, "PulseSource")
    assert hasattr(ports, "AnchorRepo")

@pytest.mark.asyncio
async def test_stubs_raise_not_implemented():
    echo = StubEchoRepo()
    trace = StubTraceRepo()
    pulse = StubPulseSource()
    anchor = StubAnchorRepo()

    with pytest.raises(NotImplementedError):
        await echo.list()

    with pytest.raises(NotImplementedError):
        await trace.list_by_correlation("cid")

    with pytest.raises(NotImplementedError):
        await pulse.now()

    with pytest.raises(NotImplementedError):
        await anchor.get_by_key("key")

@pytest.mark.asyncio
async def test_di_check_route_reports_stub_classes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/dev/di-check")
        assert r.status_code == 200
        body = r.json()
        assert body["echo_repo"] == "StubEchoRepo"
        assert body["trace_repo"] == "StubTraceRepo"
        assert body["pulse_source"] == "StubPulseSource"
        assert body["anchor_repo"] == "StubAnchorRepo"
