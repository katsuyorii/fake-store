from pydantic import BaseModel, EmailStr, Field, field_validator

from datetime import datetime

from core.utils.validators import validate_phone_number_format, validate_password_complexity

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

class UserChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_complexity(value)

class UserChangeEmailSchema(BaseModel):
    new_email: EmailStr

class UserAddressesResponseSchema(BaseModel):
    id: int
    city: str
    street: str
    flat: int
    entrance: int | None
    floot: int | None
    intercom: str | None

class UserAddressCreateSchema(BaseModel):
    city: str
    street: str
    flat: int
    entrance: int | None = Field(default=None)
    floot: int | None = Field(default=None)
    intercom: str | None = Field(default=None)