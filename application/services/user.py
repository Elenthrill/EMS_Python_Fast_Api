from domain.models.user import User, Role, IUserRepository
from dto.user import UserResponse
from core.security import hash_password


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self._to_response(user)

    async def update_user_role(self, login: str, new_role: Role) -> UserResponse:
        user = await self.user_repo.get_by_login(login)
        if not user:
            raise ValueError("User not found")
        if user.role == Role.ADMIN:
            raise PermissionError("Cannot modify an ADMIN user")
        user.role = new_role
        saved = await self.user_repo.save(user)
        return self._to_response(saved)

    def _to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            login=user.login,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )
