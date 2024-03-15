from abc import ABC, abstractmethod
from typing import List, Any, Tuple
from fastapi import Request


class FilterGetInstanceNotSupportedError(Exception):
    pass


class BaseFilterBackend(ABC):
    """
    A base class from which all filter backend classes should inherit.
    """

    @abstractmethod
    async def filter_queryset(self, request: Request, data: List[Any]):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")

    async def _get_instance(self, field_names: List[str], instance: object) -> Tuple[str, object]:
        """
        Returns the field and foreign key object.
        """
        raise NotImplementedError("If you want to get access of foreign key object you have to implement this method")
