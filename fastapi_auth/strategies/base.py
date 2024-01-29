from abc import ABC, abstractmethod
from typing import Generic, Optional
from fastapi_auth.models import user_model, token_model


class StrategyDestroyNotSupportedError(Exception):
    pass


class Strategy(ABC, Generic[user_model, token_model]):

    @abstractmethod
    async def read_token(self, token: Optional[str]) -> Optional[user_model]:
        raise NotImplementedError

    @abstractmethod
    async def get_token_by_user(self, user: user_model) -> Optional[token_model]:
        raise NotImplementedError

    @abstractmethod
    async def destroy_token(self, token: str, user: user_model) -> None:
        raise NotImplementedError
