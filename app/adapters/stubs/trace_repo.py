from typing import Iterable
from app.domain.models import Trace
from app.domain.ports import TraceRepo

MSG = "StubTraceRepo: implementação real será plugada nas Etapas 3/5."

class StubTraceRepo(TraceRepo):
    async def save(self, trace: Trace) -> Trace:
        raise NotImplementedError(MSG)
    async def list_by_correlation(self, correlation_id: str, limit: int = 100) -> Iterable[Trace]:
        raise NotImplementedError(MSG)
