from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    duration_minutes: int
    price: Decimal
    is_medical: bool = False
    description: str | None = None


class ServiceCreate(ServiceBase):
    tenant_id: UUID


class ServiceRead(ServiceBase):
    id: UUID
    tenant_id: UUID

    class Config:
        orm_mode = True
