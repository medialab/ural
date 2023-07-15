from typing import Optional, List, Union, Dict, Callable, Any

from ural.types import QueryArgValue

FormatArgValueCallable = Callable[[str, QueryArgValue], Any]
Path = Union[str, List[Union[str, int]]]

def format_url(
    base_url: str,
    path: Optional[Path] = ...,
    args: Optional[Dict[str, Any]] = ...,
    format_arg_value: Optional[FormatArgValueCallable] = ...,
    fragment: Optional[str] = ...,
    ext: Optional[str] = ...,
) -> str: ...

class URLFormatter(object):
    BASE_URL = Optional[str]
    def __init__(
        self,
        base_url: Optional[str] = ...,
        path: Optional[Path] = ...,
        args: Optional[Dict[str, Any]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ): ...
    def __call__(
        self,
        base_url: Optional[str] = ...,
        path: Optional[Path] = ...,
        args: Optional[Dict[str, Any]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ) -> str: ...
    def format_arg_value(self, key: str, value: Any) -> QueryArgValue: ...
    def format(
        self,
        base_url: Optional[str] = ...,
        path: Optional[Path] = ...,
        args: Optional[Dict[str, Any]] = ...,
        format_arg_value: Optional[FormatArgValueCallable] = ...,
        fragment: Optional[str] = ...,
        ext: Optional[str] = ...,
    ) -> str: ...
