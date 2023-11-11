from abc import ABC
from typing import Generic, Optional

from fastapi_auth.managers.base import BaseUserManager
from fastapi_auth.models import user_model


class StrategyDestroyNotSupportedError(Exception):
    pass


class Strategy(ABC, Generic[user_model]):

    async def read_token(
            self, token: Optional[str], user_manager: BaseUserManager[user_model]
    ) -> Optional[user_model]:
        raise NotImplementedError

    async def write_token(self, user: user_model) -> str:
        raise NotImplementedError

    async def destroy_token(self, token: str, user: user_model) -> None:
        raise NotImplementedError
