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

    def __call__(self, *args, **kwargs):
        if self.__name__ == 'AbstractToken':
            raise TypeError(f"Cannot instantiate class {self.__name__}")
        return super().__call__(*args, **kwargs)

    async def save(self, created: bool = False, **kwargs):
        raise NotImplementedError

    async def delete(self, **kwargs):
        raise NotImplementedError(f"FastApiAuth doesn't provide a DB representation for {self.__class__.__name__}.")

    @classmethod
    async def create(cls, **kwargs):
        raise NotImplementedError(f"FastApiAuth doesn't provide a DB representation for {cls.__class__.__name__}.")

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


token_model = TypeVar("token_model", bound=AbstractToken)
