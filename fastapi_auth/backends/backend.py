from fastapi_auth.backends.base import BaseBackend
from fastapi_auth.models import user_model
from fastapi_auth.repositories import user_repository


class Backend(BaseBackend[user_model, user_repository]):
    ...
