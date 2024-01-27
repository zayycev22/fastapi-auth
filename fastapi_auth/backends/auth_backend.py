from typing import Optional

from fastapi_auth.backends.base import BaseBackend
from fastapi_auth.hasher import Hasher
from fastapi_auth.models import user_model
from fastapi_auth.strategies.base import Strategy


class AuthBackend(BaseBackend[user_model]):
    async def authenticate(self, username: str, password: str, **kwargs) -> Optional[user_model]:
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None and password is None:
            return None
        user = await self.user_repo.get_by_natural_key(username)
        if user is None:
            Hasher.get_password_hash(password)
            return None
        if user.user_can_authenticate() and user.check_password(password):
            return user
        return None

    async def login(self, strategy: Strategy, user: user_model):
        # todo Убрать создание токена -> получение токена и если его нет, то создать
        token = await strategy.get_token(user)
        return await self.transport.get_login_data(token)

    async def logout(self, strategy: Strategy):
        pass
