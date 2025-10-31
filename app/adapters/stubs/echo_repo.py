from typing import Iterable, Optional
from uuid import UUID

from app.domain.models import Echo
from app.domain.ports import EchoRepo

MSG = "StubEchoRepo: implementação real será plugada nas Etapas 3/5."

class StubEchoRepo(EchoRepo):
    async def save(self, echo: Echo) -> Echo:
        raise NotImplementedError(MSG)
    async def get(self, echo_id: UUID) -> Optional[Echo]:
        raise NotImplementedError(MSG)
    async def list(self, kind: Optional[str] = None, limit: int = 50) -> Iterable[Echo]:
        raise NotImplementedError(MSG)
    async def exists_idempotency(self, key: str) -> bool:
        raise NotImplementedError(MSG)