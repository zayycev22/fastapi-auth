from datetime import datetime
from typing import Optional
import jwt
from fastapi_auth.jwt import decode_jwt, encode_jwt
from fastapi_auth.models import user_model
from fastapi_auth.repositories import user_repository
from fastapi_auth.strategies.base import Strategy, StrategyDestroyNotSupportedError


class JwtStrategy(Strategy[user_model, None]):
    def __init__(self, secret_key: str, user_repo: user_repository, lifetime_seconds: int = 3600,
                 algorithm: str = "HS256"):
        self.lifetime_seconds = lifetime_seconds
        self.algorithm = algorithm
        self.user_repo = user_repo
        self.secret_key = secret_key

    async def read_token(self, token: Optional[str]) -> Optional[user_model]:
        try:
            data = decode_jwt(secret=self.secret_key, token=token)
        except jwt.PyJWTError:
            return None
        else:
            lifetime = data.get("exp")
            if lifetime > datetime.now().timestamp():
                return None
            user_id = data.get('id')
            user = await self.user_repo.get(id=user_id)
            return user

    async def get_token_by_user(self, user: user_model) -> str:
        data = {"id": user.id, "password": user.password}
        return encode_jwt(data, secret=self.secret_key, lifetime_seconds=self.lifetime_seconds)

    async def destroy_token(self, token: str, user: user_model) -> None:
        raise StrategyDestroyNotSupportedError("A JWT can't be invalidated: it's valid until it expires.")
