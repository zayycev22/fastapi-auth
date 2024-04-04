from typing import Set, Type, Optional, Sequence
from pydantic import BaseModel, Field, create_model
from fastapi import Request
from fastapi_auth.filters.base import BaseFilterBackend


class SearchFilter(BaseFilterBackend):
    search_param = 'search'

    def __init__(self, *search_fields: str):
        self.search_fields = search_fields

    async def filter_queryset(self, request: Request, data: Sequence[object]) -> Sequence[object]:
        param = request.query_params.get(self.search_param)
        queryset = set()
        if param is not None:
            for item in data:
                await self._inspect_item(item, param, queryset)
            return list(queryset)
        return data

    async def _inspect_item(self, item: object, param: str, queryset: Set) -> None:
        for search_field in self.search_fields:
            if "__" in search_field:
                search_field1, sub_item = await self._get_instance(search_field.split("__"), item)
                if sub_item is None:
                    continue
                self._check_item(item, search_field1, queryset, param, sub_item)
            else:
                self._check_item(item, search_field, queryset, param)

    def _check_item(self, item: object, search_field: str, queryset: Set, param: str, sub_item: object = None):
        obj = sub_item if sub_item is not None else item
        if hasattr(obj, search_field):
            if param.lower() in str(getattr(obj, search_field, "")).lower().strip():
                queryset.add(item)
        else:
            raise AttributeError(f"{obj} has no attribute {search_field}")

    @classmethod
    def request_schema(cls) -> Type[BaseModel]:
        request_schema = {
            cls.search_param: (Optional[str], Field(default=None)),
        }
        return create_model(f"{cls.__name__.split('.')[-1]}", **request_schema)
