from abc import ABC
from typing import Generic, Optional, Type

from fastapi_auth.models import token_model
from fastapi_auth.models.user import user_model


class BaseTokenRepository(ABC, Generic[token_model]):
    def __init__(self, tm: Type[token_model]):
        self.token_model = tm

    async def create(self, **kwargs) -> token_model:
        raise NotImplementedError

    async def get_by_key(self, key: str) -> Optional[token_model]:
        raise NotImplementedError

    async def delete(self, token: token_model) -> None:
        raise NotImplementedError


class BaseUserRepository(ABC, Generic[user_model]):
    def __init__(self, model: Type[user_model], token_repo: BaseTokenRepository):
        self.user_model = model
        self.token_repo = token_repo

    async def get(self, **kwargs) -> Optional[user_model]:
        raise NotImplementedError

    async def create(self, **kwargs) -> user_model:
        raise NotImplementedError

    async def get_by_natural_key(self, natural_key) -> Optional[user_model]:
        raise NotImplementedError
