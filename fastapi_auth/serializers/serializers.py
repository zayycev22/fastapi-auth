import inspect
from typing import Union, List, Sequence, Any
from pydantic import BaseModel
from fastapi_auth.exceptions import ValidationError
from fastapi_auth.serializers.base import BaseSerializer, base_serializer


class Serializer(BaseSerializer):

    def __init__(self, instance: Union[object, Sequence[object]], many: bool = False):
        super(Serializer, self).__init__(instance, many)

    async def _parse_data(self) -> Union[dict, List[dict]]:
        if self._many:
            return await self._parse_many_instances(self._instance)
        else:
            return await self._parse_single_instance(self._instance)

    async def _parse_methods(self, methods: list[tuple], annotations: dict) -> dict:
        data = {}
        for method in methods:
            key, value = method
            try:
                if key.startswith("get_") and key[4:] in annotations:
                    data[key[4:]] = value
            except IndexError:
                raise ValidationError(f"Invalid method {key}")
        return data

    async def _parse_single_instance(self, instance: object) -> dict:
        data = {}
        fields = self._get_annotations()
        methods = inspect.getmembers(self, predicate=inspect.iscoroutinefunction)
        parsed_methods = await self._parse_methods(methods, fields)
        for key in fields:
            if key in parsed_methods:
                method_field = await parsed_methods[key](instance)
                if method_field is None:
                    data[key] = None
                    continue
                is_base_model, is_list = await self._check_type(fields[key], method_field)
                if is_base_model:
                    serializer = self._get_serializer(key)
                    d = await serializer(instance=method_field, many=is_list).data
                    data[key] = d
                else:
                    data[key] = method_field
            else:
                try:
                    data[key] = instance.__dict__[key]
                except KeyError:
                    raise ValidationError(f"Check field {key}")
        return data

    async def _parse_many_instances(self, instances: List[object]) -> List[dict]:
        data = []
        for instance in instances:
            d = await self._parse_single_instance(instance)
            data.append(d)
        return data

    async def _check_type(self, annotation: type, method_field: Any) -> tuple[bool, bool]:
        try:
            return issubclass(annotation, BaseModel), isinstance(method_field, Sequence)
        except TypeError:
            return issubclass(annotation.__args__[0], BaseModel), isinstance(method_field, Sequence)

    def _get_serializer(self, key: str) -> base_serializer:
        return getattr(self, key)

    @classmethod
    def _get_annotations(cls):
        return cls.__annotations__
