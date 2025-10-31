from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

@dataclass(frozen=True)
class Context:
    correlation_id: str
    actor: Optional[str] = None
    tenant_id: Optional[str] = None
    
@dataclass(frozen=True)
class Anchor:
    id: Optional[UUID]
    key: str
    kind: str
    meta: dict[str, Any] | None = None
    version: int = 1
    
@dataclass(frozen=True)
class Echo:
    id: Optional[UUID]
    kind: str
    payload: dict[str, Any]
    anchor_id: Optional[UUID] = None
    correlation_id: Optional[str] = None
    
@dataclass(frozen=True)    
class Trace:
    id: Optional[UUID]
    span: str
    attrs: dict[str, Any] | None = None
    correlation_id: Optional[str] = None
    
@dataclass(frozen=True)
class Pulse:
    ts: str
    sequence: Optional[int] = None
    