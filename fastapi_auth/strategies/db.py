from typing import Optional

from fastapi_auth.models import token_model, user_model, AnonymousUser
from fastapi_auth.repositories import BaseTokenRepository, BaseUserRepository
from fastapi_auth.strategies.base import Strategy


class DbStrategy(Strategy[user_model, token_model]):
    def __init__(self, token_repo: BaseTokenRepository, user_repo: BaseUserRepository):
        self._token_repo = token_repo
        self._user_repo = user_repo

    async def read_token(self, token: str) -> user_model:
        access_token = await self._token_repo.get_by_key(token)
        if access_token is None:
            return AnonymousUser()
        user = await self._user_repo.get(id=access_token.user_id)
        return user

    async def get_token_by_user(self, user: user_model) -> Optional[token_model]:
        access_token = await self._token_repo.get_by_user_id(user_id=user.id)
        return access_token

    async def destroy_token(self, token: str, user: user_model) -> None:
        access_token = await self._token_repo.get_by_key(token)
        if access_token is not None:
            await self._token_repo.delete(access_token)
