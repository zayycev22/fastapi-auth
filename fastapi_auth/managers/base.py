from abc import ABC, abstractmethod
from typing import Generic, Optional
import unicodedata
from fastapi_auth.hasher import Hasher
from fastapi_auth.models import user_model
from fastapi_auth.repositories.base import user_repository


class BaseUserManager(ABC, Generic[user_model, user_repository]):
    def __init__(self, repo: user_repository):
        self._user_repo = repo
        self._hasher = Hasher()

    @abstractmethod
    async def on_user_created(self, user: user_model) -> None:
        raise NotImplementedError

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    async def get(self, **kwargs) -> Optional[user_model]:
        user = await self._user_repo.get(**kwargs)
        return user

    async def _create_user(self, **kwargs) -> user_model:
        if self._user_repo.user_model.USERNAME_FIELD not in kwargs:
            raise ValueError("The given username must be set")
        user = await self._user_repo.create(**kwargs)
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

    async def get_by_natural_key(self, natural_key: str) -> Optional[user_model]:
        user = await self._user_repo.get_by_natural_key(natural_key)
        return user
