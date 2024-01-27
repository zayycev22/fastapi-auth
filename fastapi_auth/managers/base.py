from abc import ABC, abstractmethod
from typing import Generic, Optional

import unicodedata

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

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    async def get(self, **kwargs) -> Optional[user_model]:
        user = await self.repo.get(**kwargs)
        return user

    async def _create_user(self, **kwargs) -> user_model:
        if self.repo.user_model.USERNAME_FIELD not in kwargs:
            raise ValueError("The given username must be set")
        user = await self.repo.create(**kwargs)
        return user

    async def create_user(self, **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", False)
        user = await self._create_user(**kwargs)
        await self.on_user_created(user)
        return user

    async def create_superuser(self, **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", True)
        user = await self._create_user(**kwargs)
        await self.on_user_created(user)
        return user

    async def get_by_natural_key(self, username: str) -> Optional[user_model]:
        user = await self.repo.get_by_natural_key(username)
        return user
