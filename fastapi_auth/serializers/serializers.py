import inspect
from typing import Union, List
from fastapi_auth.exceptions import ValidationError
from fastapi_auth.serializers.base import BaseSerializer


class Serializer(BaseSerializer):

    def __init__(self, instance: Union[object, List[object]], many: bool = False):
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
        fields = self.__annotations__
        methods = inspect.getmembers(self, predicate=inspect.iscoroutinefunction)
        parsed_methods = await self._parse_methods(methods, fields)
        for key in fields:
            if key in parsed_methods:
                data[key] = await parsed_methods[key](instance)
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
