from abc import ABC
from typing import TypeVar, Generic

from pydantic import BaseModel

schema_detail_type = TypeVar("schema_detail_type")


class AbstractDefaultSchema(BaseModel, ABC, Generic[schema_detail_type]):
    pass


class DefaultSchema(AbstractDefaultSchema[schema_detail_type]):
    status: str
    detail: schema_detail_type
