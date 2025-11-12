from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.service import ServiceRead


class StaffBase(BaseModel):
    full_name: str
    role: str
    is_active: bool = True
    service_ids: list[UUID] = Field(default_factory=list)


class StaffCreate(StaffBase):
    tenant_id: UUID


class StaffRead(BaseModel):
    id: UUID
    tenant_id: UUID
    full_name: str
    role: str
    is_active: bool
    services: list[ServiceRead]

    class Config:
        orm_mode = True
