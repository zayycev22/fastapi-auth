import binascii
import datetime
import os
from abc import ABCMeta
from typing import TypeVar, Protocol


class AbstractToken:
    id: int
    user_id: int
    time_created: datetime.datetime
    key: str

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'AbstractToken':
            raise TypeError(f"Cannot instantiate class {cls.__name__}")
        return super().__call__(*args, **kwargs)

    async def save(self, created: bool = False, **kwargs):
        raise NotImplementedError

    async def delete(self, **kwargs):
        raise NotImplementedError

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


token_model = TypeVar("token_model", bound=AbstractToken)
