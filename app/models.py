from datetime import date, datetime
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from typing import Literal, Optional
from uuid import uuid4

class ProcessingStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class ObligationStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"
    na = "na"


class Citation(BaseModel):
    page: int = 1
    quote: str
    quote: str = Field(min_length=1, max_length=1000)

    value: str
    confidence: float
    confidence: float = Field(ge=0, le=1)
    citation: Citation
    category: str
    severity: str
    explanation: str
    recommendation: str
    severity: Literal["high", "medium", "low"]
    explanation: str = Field(min_length=1, max_length=500)
    recommendation: str = Field(min_length=1, max_length=500)
    citation: Citation
    owner: Optional[str] = None
    status: str = "open"
    confidence: float = 0.8
    status: ObligationStatus = ObligationStatus.open
    confidence: float = Field(default=0.8, ge=0, le=1)
    citation: Citation

class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    entity_type: str
    entity_id: str
    action: str
    before: dict | None = None
    after: dict | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Contract(BaseModel):
    contract_type: str = "MSA"
    processing_status: str = "ready"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processing_status: ProcessingStatus = ProcessingStatus.queued
    processing_error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_text: str = ""
    clauses: list[Clause] = []
    extractions: list[Extraction] = []
    risks: list[RiskFlag] = []
    obligations: list[Obligation] = []
    clauses: list[Clause] = Field(default_factory=list)
    extractions: list[Extraction] = Field(default_factory=list)
    risks: list[RiskFlag] = Field(default_factory=list)
    obligations: list[Obligation] = Field(default_factory=list)
    summary: str = ""
    audit_log: list[AuditEvent] = Field(default_factory=list)
