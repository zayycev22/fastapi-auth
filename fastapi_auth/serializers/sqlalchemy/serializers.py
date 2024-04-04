from typing import Sequence, Optional
from sqlalchemy.orm import class_mapper, Relationship
from typing_extensions import Union
from fastapi_auth.serializers import Serializer


class ModelSerializer(Serializer):
    """
    ModelSerializer only for sqlalchemy models
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
        mapper = class_mapper(cls.Meta.model)
        annotations = cls.__annotations__
        for prop in mapper.iterate_properties:
            if prop.key not in annotations:
                if not isinstance(prop, Relationship):
                    if fields != "__all__":
                        if prop.key in fields:
                            try:
                                if prop.columns[0].expression.nullable:
                                    annotations[prop.columns[0].description] = Optional[prop.columns[0].type.python_type]
                                else:
                                    annotations[prop.columns[0].description] = prop.columns[0].type.python_type
                            except NotImplementedError:
                                raise TypeError(f"Unknown type {prop.key}")
                    else:
                        try:
                            if prop.columns[0].expression.nullable:
                                annotations[prop.columns[0].description] = Optional[prop.columns[0].type.python_type]
                            else:
                                annotations[prop.columns[0].description] = prop.columns[0].type.python_type
                        except NotImplementedError:
                            raise TypeError(f"Unknown type {prop.key}")
        class_annotations = cls.__annotations__
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
