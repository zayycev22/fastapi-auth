from typing import Sequence
from typing_extensions import Union
from fastapi_auth.serializers import Serializer


class ModelSerializer(Serializer):
    """
    ModelSerializer only for tortoise models
    """

    def __init__(self, instance: Union[object, Sequence[object]], many: bool = False):
        super(ModelSerializer, self).__init__(instance, many)

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
