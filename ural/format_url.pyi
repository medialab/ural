from typing import Optional, List, Union, Dict, Callable

ArgValue = Optional[Union[str, int, float, bool]]
FormatArgCallable = Callable[[str, ArgValue], ArgValue]

def format_url(
    base_url: str,
    path: Optional[Union[List[str], str]] = ...,
    args: Optional[Dict[str, ArgValue]] = ...,
    format_arg_value: Optional[FormatArgCallable] = ...,
    fragment: Optional[str] = ...,
) -> str: ...

class URLFormatter(object):
    BASE_URL = Optional[str]
    def __init__(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, ArgValue]] = ...,
        format_arg_value: Optional[FormatArgCallable] = ...,
        fragment: Optional[str] = ...,
    ): ...
    def __call__(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, ArgValue]] = ...,
        format_arg_value: Optional[FormatArgCallable] = ...,
        fragment: Optional[str] = ...,
    ) -> str: ...
    def format(
        self,
        base_url: Optional[str],
        path: Optional[Union[List[str], str]] = ...,
        args: Optional[Dict[str, ArgValue]] = ...,
        format_arg_value: Optional[FormatArgCallable] = ...,
        fragment: Optional[str] = ...,
    ) -> str: ...
