from pydantic import EmailStr, Field, field_validator, model_validator
from datetime import date
from typing import Optional
from base_class import ORMModel

class UserCreate(ORMModel):
    """Схема для регистрации нового пользователя"""
    login: str = Field(min_length=6, max_length=256,)

    password: str = Field(min_length=8,)

    email: Optional[EmailStr] = Field(None)
    phonenumber: Optional[str] = Field(
        None,
        pattern='^\\+\\d{11,15}$',
    )
    nickname: str = Field(None, max_length=512)
    birthdate: date
    first_name: str = Field(min_length=2, max_length=256)
    surname: str = Field(min_length=2, max_length=256)
    second_name: Optional[str] = Field(None, max_length=256)

    @field_validator("nickname", mode="before")
    @classmethod
    def validate_nickname(cls, v):
        """Валидация псевдонима для пользователя"""
        if v.isdigit():
            raise ValueError("Nickname must have at least one letter")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        """Дополнительная валидация пароля"""
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def validate_email_or_phonenumber(self):
        """Проверка, что введён или email, или phonenumber"""

        if self.email is None and self.phonenumber is None:
            raise ValueError("Must specify either email or phonenumber")

        return self

    @model_validator(mode="after")
    def create_nickname(self):
        if self.nickname is None:
            self.nickname = self.surname + ' ' + self.firstname[0] + '.'
            if self.second_name is not None:
                self.nickname += ' ' + self.second_name[0] + '.'
        return self

class UserResponse(ORMModel):
    """Схема для ответа API"""
    user_id: int
    login: str
    nickname: str

class UserUpdate(ORMModel):
    """Схема для обновления данных"""
    user_id: int
    nickname: Optional[str] = Field(None, min_length=2, max_length=512)
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=256)
    surname: Optional[str] = Field(None, min_length=2, max_length=256)
    second_name: Optional[str] = Field(None, max_length=256)

class UserChangePass(ORMModel):
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
    def check_passwords_match(self):
        """Проверка совпадения паролей"""
        if self.old_password == self.new_password:
            raise ValueError("Old and new passwords must be different")

        if self.new_password != self.confirm_password:
            raise ValueError("Passwords must match")

        return self