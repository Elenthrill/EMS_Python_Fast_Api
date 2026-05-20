from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class Role(str, Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"


class AssignableRole(str, Enum):
    MODERATOR = "MODERATOR"
    USER = "USER"


@dataclass
class User:
    id: int
    login: str
    password_hash: str
    email: str
    role: Role
    is_active: bool = True


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...
    @abstractmethod
    async def get_by_login(self, login: str) -> User | None: ...
    @abstractmethod
    async def save(self, user: User) -> User: ...
    @abstractmethod
    async def delete(self, user_id: int) -> bool: ...
