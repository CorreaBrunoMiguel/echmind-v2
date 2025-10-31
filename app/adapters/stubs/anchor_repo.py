from typing import Optional
from app.domain.models import Anchor
from app.domain.ports import AnchorRepo

MSG = "StubAnchorRepo: implementação real será plugada nas Etapas 3/5."

class StubAnchorRepo(AnchorRepo):
    async def upsert(self, key: str, kind: str, meta: dict | None = None) -> Anchor:
        raise NotImplementedError(MSG)
    async def get_by_key(self, key: str) -> Optional[Anchor]:
        raise NotImplementedError(MSG)
