from abc import ABC
from typing import Generic, Optional
from fastapi_auth.hasher import Hasher
from fastapi_auth.models import user_model, token_model
from fastapi_auth.repositories.base import user_repository
from fastapi_auth.strategies.base import Strategy


class BaseBackend(ABC, Generic[user_model, user_repository]):
    def __init__(self, user_repo: user_repository,
                 strategy: Strategy[user_model, user_repository]):
        self.user_repo = user_repo
        self.strategy = strategy

    async def authenticate(self, username=None, password=None, **kwargs) -> Optional[user_model]:
        if username is None:
            username = kwargs.get(self.user_repo.user_model.USERNAME_FIELD)
        if username is None and password is None:
            return None
        user: user_model = await self.user_repo.get_by_natural_key(username)
        if user is None:
            Hasher.get_password_hash(password)
            return None
        if user.user_can_authenticate and user.check_password(password):
            return user
        return None

    async def get_user_by_token(self, token: str) -> Optional[user_model]:
        return await self.strategy.read_token(token)

    async def get_token_by_user(self, user: user_model) -> str:
        return await self.strategy.get_token_by_user(user)
