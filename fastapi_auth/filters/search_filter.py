from typing import Set, Type, Optional, Sequence
from pydantic import BaseModel, Field, create_model
from fastapi import Request
from fastapi_auth.filters.base import BaseFilterBackend


class SearchFilter(BaseFilterBackend):
    search_param = 'search'

    def __init__(self, *search_fields: str):
        self.search_fields = search_fields

    def filter_queryset(self, request: Request, data: Sequence[object]) -> Sequence[object]:
        param = request.query_params.get(self.search_param)
        queryset = set()
        if param is not None:
            for item in data:
                self._inspect_item(item, param, queryset)
            return list(queryset)
        return data

    def _inspect_item(self, item: object, param: str, queryset: Set) -> None:
        for search_field in self.search_fields:
            if hasattr(item, search_field):
                if param in str(getattr(item, search_field)).lower().strip():
                    queryset.add(item)
            else:
                raise AttributeError(f"No such attribute {search_field}")

    @classmethod
    def request_schema(cls) -> Type[BaseModel]:
        request_schema = {
            cls.search_param: (Optional[str], Field(default=None)),
        }
        return create_model(f"{cls.__name__.split(".")[-1]}", **request_schema)
