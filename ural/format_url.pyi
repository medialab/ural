from typing import Optional, List, Union, Dict, Callable

from ural.types import QueryArgValue

FormatArgValueCallable = Callable[[str, QueryArgValue], QueryArgValue]

def format_url(
    base_url: str,
    path: Optional[Union[List[str], str]] = ...,
    args: Optional[Dict[str, QueryArgValue]] = ...,
    format_arg_value: Optional[FormatArgValueCallable] = ...,
    fragment: Optional[str] = ...,
    ext: Optional[str] = ...,
) -> str: ...

class URLFormatter(object):
    BASE_URL = Optional[str]
    def __init__(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, QueryArgValue]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ): ...
    def __call__(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, QueryArgValue]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ) -> str: ...
    def format_arg_value(self, key: str, value: QueryArgValue) -> QueryArgValue: ...
    def format(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, QueryArgValue]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ) -> str: ...
