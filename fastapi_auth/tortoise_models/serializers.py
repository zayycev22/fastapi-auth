import inspect
from typing import List, Type
from pydantic import BaseModel, create_model, ConfigDict
from typing_extensions import Union
from fastapi_auth.exceptions import ValidationError
from fastapi_auth.serializers import Serializer


class ModelSerializer(Serializer):
    """
    ModelSerializer only for tortoise models
    """
    def __init__(self, instance: Union[object, List[object]], many: bool = False):
        super(ModelSerializer, self).__init__(instance, many)

    async def _parse_single_instance(self, instance: object) -> dict:
        data = {}
        fields = self._get_annotations()
        methods = inspect.getmembers(self, predicate=inspect.iscoroutinefunction)
        parsed_methods = await self._parse_methods(methods, fields)
        for key in fields:
            if key in parsed_methods:
                data[key] = await parsed_methods[key](instance)
            else:
                try:
                    data[key] = instance.__dict__[key]
                except KeyError:
                    raise ValidationError(f"Check key {key}")
        return data

    @classmethod
    def response_schema(cls, many: bool = False) -> Union[Type[BaseModel], Type[List[Type[BaseModel]]]]:
        model_annotations = cls._get_annotations()
        dynamic_model_fields = {}
        for field_name, field_type in model_annotations.items():
            dynamic_model_fields[field_name] = (field_type, ...)
        model: Type[BaseModel] = create_model(f"{cls.__name__.split('.')[-1]}Model", **dynamic_model_fields,
                                              model_config=ConfigDict(arbitrary_types_allowed=True))
        if many:
            return List[model]
        return model

    @classmethod
    def _get_annotations(cls):
        assert hasattr(cls, 'Meta'), (
            'Class {serializer_class} missing "Meta" attribute'.format(
                serializer_class=cls.__class__.__name__
            )
        )
        assert hasattr(cls.Meta, 'model'), (
            'Class {serializer_class} missing "Meta.model" attribute'.format(
                serializer_class=cls.__class__.__name__
            )
        )
        assert hasattr(cls.Meta, 'fields'), (
            'Class {serializer_class} missing "Meta.fields" attribute'.format(
                serializer_class=cls.__class__.__name__
            )
        )

        fields = cls.Meta.fields

        annotations = {name: field.field_type for name, field in cls.Meta.model._meta.fields_map.items()}
        keys = [key for key, value in annotations.items() if value is None]
        class_annotations = cls.__annotations__
        for key in keys:
            del annotations[key]
        if fields == "__all__":
            return annotations | class_annotations
        else:
            d = {}
            for field in fields:
                try:
                    d[field] = annotations[field]
                except KeyError:
                    if field in class_annotations:
                        d[field] = class_annotations[field]
                    else:
                        raise ValueError(f"No such field {field} in model {cls.Meta.model.__name__}")
            return d

    class Meta:
        pass