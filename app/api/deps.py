from app.adapters.stubs.echo_repo import StubEchoRepo
from app.adapters.stubs.trace_repo import StubTraceRepo
from app.adapters.stubs.pulse_source import StubPulseSource
from app.adapters.stubs.anchor_repo import StubAnchorRepo

def get_echo_repo():
    return StubEchoRepo()

def get_trace_repo():
    return StubTraceRepo()

def get_pulse_source():
    return StubPulseSource()

def get_anchor_repo():
    return StubAnchorRepo()
