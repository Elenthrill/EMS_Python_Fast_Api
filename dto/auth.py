from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    login: str
    password: str
    email: EmailStr


class LoginRequest(BaseModel):
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
