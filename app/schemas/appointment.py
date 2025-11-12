from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    client_id: UUID
    staff_id: UUID
    service_id: UUID
    start_datetime: datetime
    status: AppointmentStatus
    room: str | None = None


class AppointmentCreate(AppointmentBase):
    tenant_id: UUID


class AppointmentRead(AppointmentBase):
    id: UUID
    tenant_id: UUID
    end_datetime: datetime

    class Config:
        orm_mode = True


class AppointmentQueryParams(BaseModel):
    tenant_id: UUID
    date: date | None = None
