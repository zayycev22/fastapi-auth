from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

from fastapi_auth.models import token_model
from fastapi_auth.models.user import user_model


class BaseTokenRepository(ABC, Generic[token_model]):
    def __init__(self, token_type: Type[token_model]):
        self.token_type = token_type

    @abstractmethod
    async def create(self, user_id: int) -> token_model:
        raise NotImplementedError

    @abstractmethod
    async def get_by_key(self, key: str) -> Optional[token_model]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, token: token_model) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[token_model]:
        raise NotImplementedError


class BaseUserRepository(ABC, Generic[user_model]):
    def __init__(self, model: Type[user_model]):
        self.user_model = model

    @abstractmethod
    async def get(self, **kwargs) -> Optional[user_model]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs) -> user_model:
        raise NotImplementedError

    @abstractmethod
    async def get_by_natural_key(self, natural_key) -> Optional[user_model]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, token: token_model) -> None:
        raise NotImplementedError


user_repository = TypeVar('user_repository', bound=BaseUserRepository)
token_repository = TypeVar('token_repository', bound=BaseTokenRepository)
