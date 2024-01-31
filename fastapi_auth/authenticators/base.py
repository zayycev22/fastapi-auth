from typing import Generic, Union, Annotated, Optional
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from typing_extensions import Doc

from fastapi_auth.backends.base import BaseBackend
from fastapi import Request, HTTPException
from fastapi_auth.models import user_model, AnonymousUser


class Authenticator(Generic[user_model]):

    def __init__(self, *, backend: BaseBackend):
        self._backend = backend

    async def process_token(self, request: Request, token: Optional[str]) -> None:
        if token is None:
            request.scope["user"] = AnonymousUser()
            return
        user = await self._backend.get_user_by_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        request.scope["user"] = user
