import functools
import inspect
from typing import Callable, Dict, Any, Union
from urllib import parse


def prepare_kwargs(callback: Callable, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    spec = inspect.getfullargspec(callback)
    if spec.varkw:
        return kwargs
    return {k: v for k, v in kwargs.items() if k in spec.args or k in spec.kwonlyargs}


def replace_query_param(url: str, key: str, val: Union[str, int]):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(url)
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[key] = [val]
    query = parse.urlencode(sorted(query_dict.items()), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def remove_query_param(url: str, key: str):
    """
    Given a URL and a key/val pair, remove an item in the query
    parameters of the URL, and return the new URL.
    """
    ...
    (scheme, netloc, path, query, fragment) = parse.urlsplit(url)
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict.pop(key, None)
    query = parse.urlencode(sorted(query_dict.items()), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


@functools.lru_cache(maxsize=512)
def _get_func_parameters(func, remove_first):
    parameters = tuple(inspect.signature(func).parameters.values())
    if remove_first:
        parameters = parameters[1:]
    return parameters


def _get_callable_parameters(meth_or_func):
    is_method = inspect.ismethod(meth_or_func)
    func = meth_or_func.__func__ if is_method else meth_or_func
    return _get_func_parameters(func, remove_first=is_method)


def method_has_no_args(meth):
    """Return True if a method only accepts 'self'."""
    count = len(
        [p for p in _get_callable_parameters(meth) if p.kind == p.POSITIONAL_OR_KEYWORD]
    )
    return count == 0 if inspect.ismethod(meth) else count == 1
