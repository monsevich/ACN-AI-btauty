from uuid import UUID
from pydantic import BaseModel

from app.models.deal import DealStage


class DealBase(BaseModel):
    client_id: UUID
    stage: DealStage
    source: str | None = None
    ai_summary: str | None = None


class DealCreate(DealBase):
    tenant_id: UUID


class DealRead(DealBase):
    id: UUID
    tenant_id: UUID

    class Config:
        orm_mode = True
