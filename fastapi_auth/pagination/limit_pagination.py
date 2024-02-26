from collections import OrderedDict
from fastapi import Request
from fastapi_auth.pagination.base import BasePagination
from fastapi_auth.serializers.base import BaseSerializer
from typing import Type, Optional
from pydantic import create_model, BaseModel, ConfigDict, Field
from fastapi_auth.utils import replace_query_param, remove_query_param


class LimitOffsetPagination(BasePagination):
    DEFAULT_LIMIT = 50

    def __init__(self, request: Request, serializer: Type[BaseSerializer]):
        self.count = 0
        self.offset = 0
        self.limit = 0
        self._serializer = serializer
        self._request = request

    offset_query_param = "offset"
    limit_query_param = "limit"

    def _paginate_queryset(self, instances: list[object]) -> list[object]:
        self.count = self.get_count(instances)
        self.limit = self._get_limit()
        self.offset = self._get_offset()
        if self.count == 0 or self.offset > self.count:
            return []
        return instances[self.offset:self.offset + self.limit]

    async def get_paginated_response(self, instances) -> OrderedDict:
        data = self._paginate_queryset(instances)
        return OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', await self._serializer(data, many=True).data)
        ])

    @classmethod
    def response_schema(cls, user_schema: Type[BaseSerializer]) -> Type[BaseModel]:
        pagination_schema = {
            'count': (Optional[int], Field(default=123)),
            'next': (Optional[str], Field(
                default=f"'http://api.example.org/accounts/?{cls.offset_query_param}=400&{cls.limit_query_param}=100'")),
            'previous': (Optional[str], Field(
                default=f"'http://api.example.org/accounts/?{cls.offset_query_param}=200&{cls.limit_query_param}=100'")),
            'results': (user_schema.response_schema(many=True), ...)
        }
        return create_model(f"{user_schema.__name__.split(".")[-1]}Pagination", **pagination_schema,
                            model_config=ConfigDict(arbitrary_types_allowed=True))

    @classmethod
    def request_schema(cls) -> Type[BaseModel]:
        request_schema = {
            cls.offset_query_param: (Optional[int], Field(default=None)),
            cls.limit_query_param: (Optional[int], Field(default=None))
        }
        return create_model(f"{cls.__name__.split(".")[-1]}", **request_schema)

    @staticmethod
    def get_count(queryset: list[object]) -> int:
        """
        Determine an object count, supporting regular lists.
        """
        return len(queryset)

    def _get_limit(self) -> int:
        try:
            limit = self._request.query_params[self.limit_query_param]
            return abs(int(limit))
        except (KeyError, ValueError):
            return abs(self.DEFAULT_LIMIT)

    def _get_offset(self) -> Optional[int]:
        try:
            offset = self._request.query_params[self.offset_query_param]
            return abs(int(offset))
        except (KeyError, ValueError):
            return 0

    def get_next_link(self) -> Optional[str]:
        if self.offset + self.limit >= self.count:
            return None
        url = str(self._request.url)
        url = replace_query_param(url, self.limit_query_param, self.limit)
        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self) -> Optional[str]:
        if self.offset <= 0:
            return None

        url = str(self._request.url)
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)
