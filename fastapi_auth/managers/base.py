from abc import ABC
from typing import Generic, Optional
import unicodedata
from fastapi_auth.hasher import Hasher
from fastapi_auth.models import user_model
from fastapi_auth.repositories.base import user_repository
from email_validator import validate_email, EmailNotValidError


class BaseUserManager(ABC, Generic[user_model, user_repository]):
    def __init__(self, repo: user_repository):
        self._user_repo = repo
        self._hasher = Hasher()

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    def _check_email_field(self) -> bool:
        if self._user_repo.user_model.USERNAME_FIELD == "email":
            return True
        return False

    async def get(self, **kwargs) -> Optional[user_model]:
        user = await self._user_repo.get(**kwargs)
        return user

    async def _create_user(self, username=None, **kwargs) -> user_model:
        if username is None:
            try:
                if self._check_email_field():
                    kwargs[self._user_repo.user_model.USERNAME_FIELD] = validate_email(
                        kwargs[self._user_repo.user_model.USERNAME_FIELD], check_deliverability=False).normalized
            except KeyError:
                raise ValueError(f"The given {self._user_repo.user_model.USERNAME_FIELD} must be set")
            except EmailNotValidError:
                raise ValueError(f"The given email is wrong")
        else:
            kwargs[self._user_repo.user_model.USERNAME_FIELD] = self.normalize_username(username)
        user = await self._user_repo.create(**kwargs)
        return user

    async def create_user(self, username=None, **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", False)
        user = await self._create_user(username, **kwargs)
        return user

    async def create_superuser(self, **kwargs) -> user_model:
        kwargs.setdefault("is_superuser", True)
        user = await self._create_user(**kwargs)
        return user

    async def get_by_natural_key(self, natural_key: str) -> Optional[user_model]:
        user = await self._user_repo.get_by_natural_key(natural_key)
        return user
