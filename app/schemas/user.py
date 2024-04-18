from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_banned: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3, serialization_alias="hashed_password")


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None)
