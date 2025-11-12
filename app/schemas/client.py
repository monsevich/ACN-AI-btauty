from uuid import UUID
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: EmailStr | None = None
    comment: str | None = None


class ClientCreate(ClientBase):
    tenant_id: UUID


class ClientRead(ClientBase):
    id: UUID
    tenant_id: UUID

    class Config:
        orm_mode = True
