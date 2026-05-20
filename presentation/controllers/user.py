from fastapi import APIRouter, Depends
from application.services.user import UserService
from dto.user import UpdateRoleRequest, UserResponse
from core.dependencies import (
    get_user_service,
    get_current_user,
    get_current_active_admin,
    get_current_active_admin_or_moderator,
)
from domain.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user  # зависимость get_current_user возвращает домен User, а Pydantic сериализует


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: User = Depends(get_current_active_admin_or_moderator),
):
    return await service.get_by_id(user_id)


@router.put("/role", response_model=UserResponse)
async def update_user_role(
    dto: UpdateRoleRequest,
    service: UserService = Depends(get_user_service),
    _: User = Depends(get_current_active_admin),
):
    return await service.update_user_role(dto.login, dto.role)
