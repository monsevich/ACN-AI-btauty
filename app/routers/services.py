from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_current_user
from app.db import get_db
from app.models.service import Service
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceRead

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceRead])
def list_services(
    tenant_id: UUID = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    services = db.query(Service).filter(Service.tenant_id == tenant_id).all()
    return services


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if service_in.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    service = Service(**service_in.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
