from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional

class StatusOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    service: str
    version: str
    correlation_id: str

class EchoIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str
    payload: dict[str, Any]
    anchor: Optional[str] = None  # anchor key (semântica)

class EchoOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    kind: str
    created_at: str
    correlation_id: str

class TraceOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    span: str
    started_at: str
    duration_ms: int
    correlation_id: Optional[str] = None

class PulseOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ts: str
    sequence: Optional[int] = None

class Problem(BaseModel):
    """RFC 7807: application/problem+json"""
    model_config = ConfigDict(extra="ignore")
    type: str = Field(default="about:blank")
    title: str
    status: int
    detail: Optional[str] = None
    instance: Optional[str] = None
    correlation_id: Optional[str] = None
