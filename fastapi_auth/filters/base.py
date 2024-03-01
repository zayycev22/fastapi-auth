from abc import ABC, abstractmethod
from typing import List, Any
from fastapi import Request


class BaseFilterBackend(ABC):
    """
    A base class from which all filter backend classes should inherit.
    """
    @abstractmethod
    def filter_queryset(self, request: Request, data: List[Any]):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")
