from pydantic import BaseModel, EmailStr, Field, field_validator

from datetime import datetime

from core.utils.validators import validate_phone_number_format

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

class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    is_mailing: bool | None = Field(default=None)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        return validate_phone_number_format(value)