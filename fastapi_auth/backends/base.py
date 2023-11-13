from abc import ABC, abstractmethod
from typing import Generic

from fastapi_auth.models import user_model
from fastapi_auth.repositories.base import BaseUserRepository
from fastapi_auth.strategies.base import Strategy
from fastapi_auth.transports.bearer import BearerTransport


class BaseBackend(ABC, Generic[user_model]):
    def __init__(self, transport: BearerTransport, user_repo: BaseUserRepository[user_model]):
        self.transport = transport
        self.user_repo = user_repo

    @abstractmethod
    async def authenticate(self, username: str, password: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def login(self, strategy: Strategy, user: user_model):
        raise NotImplementedError

    @abstractmethod
    async def logout(self, strategy: Strategy):
        raise NotImplementedError
