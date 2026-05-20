from fastapi import APIRouter, Depends
from application.services.auth import AuthService
from dto.auth import RegisterRequest, LoginRequest
from dto.auth import TokenResponse
from core.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(
    dto: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    return await service.register(dto)


@router.post("/login", response_model=TokenResponse)
async def login(dto: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return await service.login(dto)
