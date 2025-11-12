from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    tenant_id: UUID
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
