import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


staff_services = Table(
    "staff_services",
    Base.metadata,
    Column("staff_id", UUID(as_uuid=True), ForeignKey("staff.id"), primary_key=True),
    Column("service_id", UUID(as_uuid=True), ForeignKey("services.id"), primary_key=True),
)


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    services = relationship(
        "Service",
        secondary=staff_services,
        backref="staff_members",
        lazy="joined",
    )
