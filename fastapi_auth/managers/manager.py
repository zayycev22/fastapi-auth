from fastapi_auth.managers.base import BaseUserManager
from fastapi_auth.models import user_model
from fastapi_auth.repositories import user_repository


class Manager(BaseUserManager[user_model, user_repository]):
    ...
