from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field

class AccessStatus(str, Enum):
    GRANTED = "LIBERADO"
    BLOCKED = "BLOQUEADO"
    EXPIRED_PAYMENT = "MENSALIDADE VENCIDA"
    INACTIVE_PLAN = "PLANO INATIVO"
    PENDING_EVALUATION = "AVALIAÇÃO VENCIDA"

class TenantConfig(BaseModel):
    name: str
    primary_color: str
    logo_url: str | None = None

class StudentBase(BaseModel):
    full_name: str
    email: str
    document: str
    plan_id: int

class Student(StudentBase):
    id: int
    is_active: bool = True
    financial_status: str = "UP_TO_DATE"
    last_access: datetime | None = None
    model_config = ConfigDict(from_attributes=True)

class AccessLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    student_id: int
    timestamp: datetime = Field(default_factory=datetime.now)
    status: AccessStatus
    responsible_user: str