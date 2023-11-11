from abc import ABC
from typing import TypeVar


class AbstractUser(ABC):
    id: int
    password: str
    is_active: bool
    is_superuser: bool

    USERNAME_FIELD: str

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def natural_key(self):
        return (self.get_username(),)


user_model = TypeVar('user_model', bound=AbstractUser)
