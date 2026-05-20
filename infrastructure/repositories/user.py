from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.user import User, Role, IUserRepository
from infrastructure.database.models import UserORM, RoleEnum


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def get_by_login(self, login: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.login == login)
        )
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def save(self, user: User) -> User:
        if user.id:
            orm = await self.session.get(UserORM, user.id)
            if not orm:
                raise ValueError("User not found")
            orm.login = user.login
            orm.password_hash = user.password_hash
            orm.email = user.email
            orm.role = RoleEnum(user.role.value)
            orm.is_active = user.is_active
        else:
            orm = UserORM(
                login=user.login,
                password_hash=user.password_hash,
                email=user.email,
                role=RoleEnum(user.role.value),
                is_active=user.is_active,
            )
            self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._to_domain(orm)

    async def delete(self, user_id: int) -> None:
        orm = await self.session.get(UserORM, user_id)
        if orm:
            await self.session.delete(orm)
            await self.session.commit()

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            id=orm.id,
            login=orm.login,
            password_hash=orm.password_hash,
            email=orm.email,
            role=Role(orm.role.value),
            is_active=orm.is_active,
        )
