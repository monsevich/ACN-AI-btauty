from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_current_user
from app.db import get_db
from app.models.service import Service
from app.models.staff import Staff
from app.models.user import User
from app.schemas.staff import StaffCreate, StaffRead

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("", response_model=list[StaffRead])
def list_staff(
    tenant_id: UUID = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    staff_members = db.query(Staff).filter(Staff.tenant_id == tenant_id).all()
    return staff_members


@router.post("", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    staff_in: StaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if staff_in.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    services = (
        db.query(Service)
        .filter(Service.id.in_(staff_in.service_ids), Service.tenant_id == staff_in.tenant_id)
        .all()
        if staff_in.service_ids
        else []
    )
    if len(services) != len(staff_in.service_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service list")

    staff_member = Staff(
        tenant_id=staff_in.tenant_id,
        full_name=staff_in.full_name,
        role=staff_in.role,
        is_active=staff_in.is_active,
        services=services,
    )
    db.add(staff_member)
    db.commit()
    db.refresh(staff_member)
    return staff_member
