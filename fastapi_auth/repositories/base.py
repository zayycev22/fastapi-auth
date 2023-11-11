from abc import ABC
from typing import Generic, Optional

from fastapi_auth.models import token_model
from fastapi_auth.models.user import user_model


class BaseUserRepository(ABC, Generic[user_model]):
    async def get(self, pk: int) -> Optional[user_model]:
        raise NotImplementedError

    async def create(self, username: str, password: str,  **kwargs) -> user_model:
        raise NotImplementedError

    async def get_by_natural_key(self, username: str) -> Optional[user_model]:
        raise NotImplementedError


class BaseTokenRepository(ABC, Generic[token_model]):
    async def create(self, user_id) -> str:
        raise NotImplementedError

    async def get_by_token(self, token: str) -> int:
        raise NotImplementedError
