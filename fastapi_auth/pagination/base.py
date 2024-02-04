from collections import OrderedDict
from typing import Type
from pydantic import BaseModel
from abc import ABC, abstractmethod
from fastapi_auth.serializers.base import BaseSerializer


class BasePagination(ABC):
    @abstractmethod
    def _paginate_queryset(self, instances: list[object]) -> list[object]:
        raise NotImplementedError('paginate_queryset() must be implemented.')

    @abstractmethod
    async def get_paginated_response(self, data: list) -> OrderedDict:
        raise NotImplementedError('get_paginated_response() must be implemented.')

    @classmethod
    @abstractmethod
    def response_schema(self, user_schema: Type[BaseSerializer]) -> Type[BaseModel]:
        raise NotImplementedError('response_schema() must be implemented.')

    @classmethod
    @abstractmethod
    def request_schema(cls) -> Type[BaseModel]:
        raise NotImplementedError('request_schema() must be implemented')
