from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from core.db_conn import get_session
from core.security import decode_access_token
from infrastructure.repositories.user import UserRepository
from application.services.auth import AuthService
from application.services.user import UserService
from domain.models.user import User, Role, AssignableRole

security = HTTPBearer()


async def get_user_repo(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


async def get_auth_service(repo=Depends(get_user_repo)):
    return AuthService(repo)


async def get_user_service(repo=Depends(get_user_repo)):
    return UserService(repo)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repo: UserRepository = Depends(get_user_repo),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload["sub"])
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


async def get_current_active_admin_or_moderator(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {Role.ADMIN, Role.MODERATOR}:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
