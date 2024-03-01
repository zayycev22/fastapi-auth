from typing import Generic, Optional
from fastapi_auth.backends.base import BaseBackend
from fastapi import Request, HTTPException
from fastapi_auth.models import user_model, AnonymousUser


class Authenticator(Generic[user_model]):
    TOKEN_PREFIX = "Token"

    def __init__(self, *, backend: BaseBackend, token_prefix: Optional[str] = None):
        self._backend = backend
        if token_prefix is not None:
            self.TOKEN_PREFIX = token_prefix

    async def process_token(self, request: Request, raw_token: Optional[str] = None) -> None:
        if raw_token is None:
            request.scope["user"] = AnonymousUser()
            return
        try:
            prefix, token = raw_token.split()
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token")
        if prefix != self.TOKEN_PREFIX:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await self._backend.get_user_by_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        request.scope["user"] = user
