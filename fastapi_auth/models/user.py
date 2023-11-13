from abc import ABC
from typing import TypeVar

from fastapi_auth.hasher import Hasher


class AbstractUser(ABC):
    id: int
    password: str
    is_active: bool
    is_superuser: bool

    USERNAME_FIELD: str

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def natural_key(self):
        return self.get_username()

    def user_can_authenticate(self):
        return self.is_active

    def check_password(self, password: str):
        return Hasher.verify_password(password, self.password)

    @classmethod
    def username_attribute(cls):
        return cls.USERNAME_FIELD


user_model = TypeVar('user_model', bound=AbstractUser)
