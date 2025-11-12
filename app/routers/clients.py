from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_current_user
from app.db import get_db
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientRead

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientRead])
def list_clients(
    tenant_id: UUID = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    clients = db.query(Client).filter(Client.tenant_id == tenant_id).all()
    return clients


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if client_in.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    client = Client(**client_in.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
