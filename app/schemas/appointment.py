from __future__ import annotations

import datetime as dt
from uuid import UUID
from pydantic import BaseModel, Field


from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    client_id: UUID
    staff_id: UUID
    service_id: UUID
    start_datetime: dt.datetime
    status: AppointmentStatus
    room: str | None = None


class AppointmentCreate(BaseModel):
    client_id: UUID
    staff_id: UUID
    service_id: UUID
    start_datetime: dt.datetime
    status: str = "planned"


class AppointmentRead(BaseModel):
    id: UUID
    client_id: UUID
    staff_id: UUID
    service_id: UUID
    start_datetime: dt.datetime
    end_datetime: dt.datetime
    status: str

    class Config:
        orm_mode = True


class AppointmentQueryParams(BaseModel):
    date: dt.date | None = None
    staff_id: UUID | None = None
    service_id: UUID | None = None
