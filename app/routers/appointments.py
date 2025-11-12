from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_current_user
from app.db import get_db
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.service import Service
from app.models.staff import Staff
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    tenant_id: UUID = Query(...),
    date_filter: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    query = db.query(Appointment).filter(Appointment.tenant_id == tenant_id)
    if date_filter:
        start_dt = datetime.combine(date_filter, datetime.min.time())
        end_dt = start_dt + timedelta(days=1)
        query = query.filter(Appointment.start_datetime >= start_dt, Appointment.start_datetime < end_dt)

    return query.all()


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if appointment_in.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    service = db.query(Service).filter(Service.id == appointment_in.service_id).first()
    client = db.query(Client).filter(Client.id == appointment_in.client_id).first()
    staff_member = db.query(Staff).filter(Staff.id == appointment_in.staff_id).first()

    if not service or service.tenant_id != appointment_in.tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service")
    if not client or client.tenant_id != appointment_in.tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid client")
    if not staff_member or staff_member.tenant_id != appointment_in.tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid staff member")

    end_datetime = appointment_in.start_datetime + timedelta(minutes=service.duration_minutes)

    appointment = Appointment(
        tenant_id=appointment_in.tenant_id,
        client_id=appointment_in.client_id,
        staff_id=appointment_in.staff_id,
        service_id=appointment_in.service_id,
        start_datetime=appointment_in.start_datetime,
        end_datetime=end_datetime,
        status=appointment_in.status,
        room=appointment_in.room,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
