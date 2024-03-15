from collections import OrderedDict
from typing import Type, Sequence
from pydantic import BaseModel
from abc import ABC, abstractmethod
from fastapi_auth.serializers.base import BaseSerializer


class BasePagination(ABC):
    @abstractmethod
    def _paginate_queryset(self, instances: Sequence[object]) -> Sequence[object]:
        raise NotImplementedError('_paginate_queryset() must be implemented.')

    @abstractmethod
    async def get_paginated_response(self, data: Sequence) -> OrderedDict:
        raise NotImplementedError('get_paginated_response() must be implemented.')

    @classmethod
    @abstractmethod
    def response_schema(cls, user_schema: Type[BaseSerializer]) -> Type[BaseModel]:
        raise NotImplementedError('response_schema() must be implemented.')

    @classmethod
    @abstractmethod
    def request_schema(cls) -> Type[BaseModel]:
        raise NotImplementedError('request_schema() must be implemented')
