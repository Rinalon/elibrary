from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    login: str = Field(min_length=6, max_length=256)
    password: str = Field(min_length=8)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 час