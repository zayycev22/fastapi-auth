from typing import Sequence, Any, Type, Optional
from pydantic import BaseModel, Field, create_model
from starlette.requests import Request
from fastapi_auth.filters.base import BaseFilterBackend


class OrderingFilter(BaseFilterBackend):
    order_query_param = "ordering"
    default_ordering = "id"

    def __init__(self, *ordering_fields):
        self.ordering_fields = ordering_fields

    def filter_queryset(self, request: Request, data: Sequence[Any]) -> Sequence[Any]:
        if len(data) == 0:
            return data
        param = request.query_params.get(self.order_query_param)
        if param is not None and self._prepare_param(param) in self.ordering_fields:
            new_data = self._order_queryset(param.strip(), data)
        else:
            new_data = self._order_queryset(self.default_ordering, data)

        return new_data

    def _prepare_param(self, param: str) -> str:
        new_param = param.strip()
        if new_param.startswith("-"):
            new_param = new_param[1:]
        return new_param

    def _order_queryset(self, param: str, data: Sequence[Any]) -> Sequence[Any]:
        if not hasattr(data[0], self._prepare_param(param)):
            raise ValueError(f"Invalid parameter {param}")
        if param.startswith("-"):
            return sorted(data, key=lambda x: getattr(x, self._prepare_param(param)), reverse=True)
        return sorted(data, key=lambda x: getattr(x, self._prepare_param(param)))

    @classmethod
    def request_schema(cls) -> Type[BaseModel]:
        request_schema = {
            cls.order_query_param: (Optional[str], Field(default=None)),
        }
        return create_model(f"{cls.__name__.split(".")[-1]}", **request_schema)
