from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Схема для регистрации нового пользователя"""
    login: str = Field(min_length=6, max_length=256,)

    password: str = Field(min_length=8,)

    email: Optional[EmailStr] = Field(None)
    phonenumber: Optional[str] = Field(
        None,
        pattern='^\\+\\d{11,15}$',
    )

    nickname: str = Field(min_length=2, max_length=512)
    first_name: Optional[str] = Field(None, max_length=256)
    surname: Optional[str] = Field(None, max_length=256)
    second_name: Optional[str] = Field(None, max_length=256)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Дополнительная валидация пароля"""
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def validate_email_or_phonenumber(self) -> "UserCreate":
        """Проверка, что введён или email, или phonenumber"""

        if self.email is None and self.phonenumber is None:
            raise ValueError("Must specify either email or phonenumber")

        return self

class UserResponse(BaseModel):
    """Схема для ответа API"""
    user_id: int
    login: str
    nickname: str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    """Схема для обновления данных"""
    nickname: Optional[str] = Field(None, min_length=2, max_length=512)
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None
    first_name: Optional[str] = Field(None, max_length=256)
    surname: Optional[str] = Field(None, max_length=256)
    second_name: Optional[str] = Field(None, max_length=256)

class UserChangePass(BaseModel):
    """Схема для обновления пароля"""
    user_id: int
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Дополнительная валидация пароля"""
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        """Проверка совпадения паролей"""
        if self.old_password == self.new_password:
            raise ValueError("Old and new passwords must be different")

        if self.new_password != self.confirm_password:
            raise ValueError("Passwords must match")

        return self