from domain.models.user import User, Role, IUserRepository
from core.security import hash_password, verify_password, create_access_token
from dto.auth import TokenResponse, RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def register(self, dto: RegisterRequest) -> TokenResponse:
        existing = await self.user_repo.get_by_login(dto.login)
        if existing:
            raise ValueError("Login already exists")
        user = User(
            id=None,
            login=dto.login,
            password_hash=hash_password(dto.password),
            email=dto.email,
            role=Role.USER,
        )
        saved = await self.user_repo.save(user)
        token = create_access_token({"sub": str(saved.id), "role": saved.role.value})
        return TokenResponse(access_token=token, token_type="bearer")

    async def login(self, dto: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_login(dto.login)
        if not user or not verify_password(dto.password, user.password_hash):
            raise ValueError("Invalid credentials")
        token = create_access_token({"sub": str(user.id), "role": user.role.value})
        return TokenResponse(access_token=token, token_type="bearer")
