from fastapi_auth.managers.base import UserManagerDependency
from fastapi_auth.models import user_model
from fastapi_auth.repositories import user_repository


class Authentication:
    def __init__(self, get_user_manager: UserManagerDependency[user_model, user_repository]):
        self.get_user_manager = get_user_manager
