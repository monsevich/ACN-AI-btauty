import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class DealStage(str, PyEnum):
    new = "new"
    consultation = "consultation"
    booked = "booked"
    done = "done"
    upsell = "upsell"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    stage = Column(Enum(DealStage, name="deal_stage"), nullable=False)
    source = Column(String, nullable=True)
    ai_summary = Column(Text, nullable=True)
