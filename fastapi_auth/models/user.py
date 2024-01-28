import datetime
from typing import TypeVar, Optional

from passlib.exc import UnknownHashError

from fastapi_auth.hasher import Hasher


class AbstractBaseUser:
    id: int
    password: str
    is_active: bool
    is_superuser: bool
    time_created: datetime.datetime

    USERNAME_FIELD: str

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'AbstractUser':
            raise TypeError(f"Cannot instantiate class {cls.__name__}")
        return super().__call__(*args, **kwargs)

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def natural_key(self) -> Optional[str]:
        return self.get_username()

    def user_can_authenticate(self) -> bool:
        return self.is_active

    def check_password(self, raw_password: str) -> bool:
        try:
            return Hasher.verify_password(raw_password, self.password)
        except UnknownHashError:
            return False

    @classmethod
    def username_attribute(cls):
        return cls.USERNAME_FIELD

    def set_unusable_password(self):
        self.password = Hasher.make_password(None)

    def set_password(self, raw_password: str) -> None:
        self.password = Hasher.make_password(raw_password)

    async def save(self, **kwargs):
        raise NotImplementedError


user_model = TypeVar('user_model', bound=AbstractBaseUser)
