import uuid

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    organization_id: uuid.UUID
    role_id: uuid.UUID
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    role_id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool