import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class AppointmentStatus(str, PyEnum):
    planned = "planned"
    confirmed = "confirmed"
    done = "done"
    canceled = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus, name="appointment_status"), nullable=False)
    room = Column(String, nullable=True)

    client = relationship("Client")
    staff = relationship("Staff")
    service = relationship("Service")
