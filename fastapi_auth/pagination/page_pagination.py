from collections import OrderedDict
from typing import Type, Optional
from pydantic import BaseModel, Field, create_model, ConfigDict
from fastapi_auth.pagination.base import BasePagination
from fastapi_auth.serializers.base import BaseSerializer
from fastapi import Request, HTTPException
from fastapi_auth.pagination.page import Paginator, InvalidPage

from fastapi_auth.utils import replace_query_param, remove_query_param


class PageNumberPagination(BasePagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    DEFAULT_PAGE_SIZE = 100
    invalid_page_message = 'Invalid page.'

    def __init__(self, request: Request, serializer: Type[BaseSerializer]):
        self._request = request
        self._serializer = serializer
        self.page = None

    def _paginate_queryset(self, instances: list[object]) -> list[object]:
        page_number = self.get_page_number()
        page_size = self.get_page_size()
        paginator = Paginator(instances, page_size, allow_empty_first_page=True)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise HTTPException(status_code=404, detail=msg)
        return list(self.page)

    async def get_paginated_response(self, instances: list[object]) -> OrderedDict:
        data = self._paginate_queryset(instances)
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', await self._serializer(data, many=True).data)
        ])

    @classmethod
    def response_schema(cls, user_schema: Type[BaseSerializer]) -> Type[BaseModel]:
        pagination_schema = {
            'count': (int, Field(default=123)),
            'next': (Optional[str], Field(
                default=f"'http://api.example.org/accounts/?{cls.page_query_param}=4'")),
            'previous': (Optional[str], Field(
                default=f"'http://api.example.org/accounts/?{cls.page_query_param}=2'")),
            'results': (user_schema.response_schema(many=True), ...)
        }
        return create_model(f"{user_schema.__name__.split(".")[-1]}Pagination", **pagination_schema,
                            model_config=ConfigDict(arbitrary_types_allowed=True))

    @classmethod
    def request_schema(cls) -> Type[BaseModel]:
        request_schema = {
            cls.page_query_param: (Optional[int], Field(default=None)),
            cls.page_size_query_param: (Optional[int], Field(default=None))
        }
        return create_model(f"{cls.__name__.split(".")[-1]}", **request_schema)

    def get_page_number(self) -> int:
        try:
            page_number = self._request.query_params[self.page_query_param]
            return abs(int(page_number))
        except (KeyError, ValueError):
            return abs(1)

    def get_page_size(self) -> int:
        if self.page_size_query_param:
            try:
                return abs(int(self._request.query_params[self.page_size_query_param]))
            except (KeyError, ValueError):
                pass
        return self.DEFAULT_PAGE_SIZE

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = str(self._request.url)
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = str(self._request.url)
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
