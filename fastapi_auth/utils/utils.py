import inspect
from typing import Callable, Dict, Any


def prepare_kwargs(callback: Callable, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    spec = inspect.getfullargspec(callback)
    if spec.varkw:
        return kwargs
    return {k: v for k, v in kwargs.items() if k in spec.args or k in spec.kwonlyargs}
