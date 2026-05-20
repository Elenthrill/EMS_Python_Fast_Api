# infrastructure/database/base_repository.py
from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

EntityT = TypeVar("EntityT")
ModelT = TypeVar("ModelT")


class BaseSQLAlchemyRepository(Generic[EntityT, ModelT]):
    """Технический хелпер, не реализует доменный интерфейс!"""

    def __init__(self, session: AsyncSession, model_cls: Type[ModelT]):
        self._session = session
        self._model_cls = model_cls

    async def _get_by_id(self, id: int) -> ModelT | None:
        result = await self._session.execute(
            select(self._model_cls).where(self._model_cls.id == id)
        )
        return result.scalar_one_or_none()

    async def _save(self, orm_obj: ModelT) -> ModelT:
        self._session.add(orm_obj)
        await self._session.commit()
        await self._session.refresh(orm_obj)
        return orm_obj

    # можно добавить другие вспомогательные методы, если нужно
    # но не заставляйте домен зависеть от них!
