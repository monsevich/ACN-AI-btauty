from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_current_user
from app.db import get_db
from app.models.client import Client
from app.models.deal import Deal
from app.models.user import User
from app.schemas.deal import DealCreate, DealRead

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("", response_model=list[DealRead])
def list_deals(
    tenant_id: UUID = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    deals = db.query(Deal).filter(Deal.tenant_id == tenant_id).all()
    return deals


@router.post("", response_model=DealRead, status_code=status.HTTP_201_CREATED)
def create_deal(
    deal_in: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if deal_in.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    client = db.query(Client).filter(Client.id == deal_in.client_id).first()
    if not client or client.tenant_id != deal_in.tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid client")

    deal = Deal(**deal_in.dict())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal
