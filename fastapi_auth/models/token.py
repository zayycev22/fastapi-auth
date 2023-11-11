import datetime
from abc import ABC
from typing import TypeVar


class Token(ABC):
    id: int
    user_id: int
    time_created: datetime.datetime


token_model = TypeVar("token_model", bound=Token)
