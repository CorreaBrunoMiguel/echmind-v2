from app.domain.models import Pulse
from app.domain.ports import PulseSource

MSG = "StubPulseSource: implementação real será plugada nas Etapas 3/5."

class StubPulseSource(PulseSource):
    async def now(self) -> Pulse:
        raise NotImplementedError(MSG)
    async def emit(self, note: str | None = None) -> Pulse:
        raise NotImplementedError(MSG)
