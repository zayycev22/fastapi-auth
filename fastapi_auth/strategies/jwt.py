from datetime import datetime
from enum import Enum
from typing import Optional
import jwt
from fastapi_auth.jwt import decode_jwt, encode_jwt
from fastapi_auth.models import user_model
from fastapi_auth.repositories import user_repository
from fastapi_auth.strategies.base import Strategy, StrategyDestroyNotSupportedError


class TokenTypes(str, Enum):
    REFRESH_TOKEN = 'refresh'
    ACCESS_TOKEN = 'access'


class JwtStrategy(Strategy[user_model, None]):
    def __init__(self, user_repo: user_repository, access_token_lifetime_seconds: int = 3600,
                 refresh_token_lifetime_seconds: int = 604800, algorithm: str = "HS256"):
        self.access_token_lifetime_seconds = access_token_lifetime_seconds
        self.refresh_token_lifetime_seconds = refresh_token_lifetime_seconds
        self.algorithm = algorithm
        self.user_repo = user_repo

    async def read_token(self, token: Optional[str]) -> Optional[user_model]:
        try:
            data = decode_jwt(token=token)
        except jwt.PyJWTError:
            return None
        else:
            lifetime = data.get("exp")
            if lifetime > datetime.now().timestamp():
                return None
            token_type = data.get("type")
            if token_type == TokenTypes.REFRESH_TOKEN:
                return None
            user_id = data.get('id')
            user = await self.user_repo.get(id=user_id)
            return user

    async def get_token_by_user(self, user: user_model) -> tuple[str, str]:
        refresh_data = {"id": user.id, "type": TokenTypes.REFRESH_TOKEN}
        access_data = {"id": user.id, "type": TokenTypes.ACCESS_TOKEN}
        return (encode_jwt(refresh_data, lifetime_seconds=self.access_token_lifetime_seconds),
                encode_jwt(access_data, lifetime_seconds=self.refresh_token_lifetime_seconds))

    async def destroy_token(self, token: str, user: user_model) -> None:
        raise StrategyDestroyNotSupportedError("A JWT can't be invalidated: it's valid until it expires.")

    async def refresh_token(self, refresh_token: str) -> Optional[str]:
        try:
            data = decode_jwt(token=refresh_token)
        except jwt.PyJWTError:
            return None
        else:
            lifetime = data.get("exp")
            if lifetime > datetime.now().timestamp():
                return None
            token_type = data.get("type")
            if token_type == TokenTypes.ACCESS_TOKEN:
                return None
        user_id = data.get('id')
        access_data = {"id": user_id, "type": TokenTypes.ACCESS_TOKEN}
        return encode_jwt(access_data, lifetime_seconds=self.access_token_lifetime_seconds)
