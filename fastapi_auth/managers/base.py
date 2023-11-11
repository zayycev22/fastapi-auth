from abc import ABC, abstractmethod
from typing import Generic, Optional

from fastapi_auth.hasher import Hasher
from fastapi_auth.models import user_model
from fastapi_auth.repositories.base import BaseUserRepository


class BaseUserManager(ABC, Generic[user_model]):
    def __init__(self, repo: BaseUserRepository[user_model]):
        self.repo = repo
        self.hasher = Hasher()

    @abstractmethod
    async def on_user_created(self, user: user_model):
        raise NotImplementedError

    async def get(self, pk: int) -> Optional[user_model]:
        user = await self.repo.get(pk)
        return user

    async def _create_user(self, username: str, password: str, **kwargs) -> user_model:
        if not username:
            raise ValueError("The given username must be set")
        password = self.hasher.get_password_hash(password)
        user = await self.repo.create(username, password,  **kwargs)
        return user

    async def create_user(self, username: str, password: str,  **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", False)
        user = await self._create_user(username, password,  **kwargs)
        await self.on_user_created(user)
        return user

    async def create_superuser(self, username: str, password: str,  **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", True)
        user = await self._create_user(username, password, **kwargs)
        await self.on_user_created(user)
        return user

    async def get_by_natural_key(self, username: str) -> Optional[user_model]:
        user = await self.repo.get_by_natural_key(username)
        return user
