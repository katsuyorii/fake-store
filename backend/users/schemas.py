from pydantic import BaseModel, EmailStr

from datetime import datetime

from .models import UserRoleEnum


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    role: UserRoleEnum
    created_at: datetime
    is_active: bool
    is_mailing: bool