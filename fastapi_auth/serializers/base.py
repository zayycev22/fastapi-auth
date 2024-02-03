from abc import ABC, abstractmethod
from typing import List, Type, Union
from pydantic import BaseModel, create_model, ConfigDict


class BaseSerializer(ABC):
    def __init__(self, instance: Union[object, List[object]], many: bool = False):
        self._instance = instance
        self._many = many

    @classmethod
    def model(cls, many: bool = False) -> Union[Type[BaseModel], Type[List[Type[BaseModel]]]]:

        annotations = cls.__annotations__
        dynamic_model_fields = {}
        for field_name, field_type in annotations.items():
            dynamic_model_fields[field_name] = (field_type, ...)
        model: Type[BaseModel] = create_model(f"{cls.__name__.split(".")[-1]}Model", **dynamic_model_fields,
                                              model_config=ConfigDict(arbitrary_types_allowed=True))
        if many:
            return List[model]
        return model

    @abstractmethod
    async def _parse_data(self) -> dict:
        raise NotImplementedError

    @property
    async def data(self) -> dict:
        return await self._parse_data()

    @abstractmethod
    async def _parse_methods(self, methods: list[tuple], annotations: dict):
        raise NotImplementedError

    @abstractmethod
    async def _parse_single_instance(self, instance: object) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def _parse_many_instances(self, instances: List[object]) -> List[dict]:
        raise NotImplementedError
