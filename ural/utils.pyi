from typing import Optional, Union, Dict, List, overload
from urllib.parse import SplitResult
from ural.types import AnyUrlTarget, Literal, QueryArgValue

def urlsplit(url: str) -> SplitResult: ...
def safe_urlsplit(url: AnyUrlTarget, scheme: Optional[str] = ...) -> SplitResult: ...
def pathsplit(urlpath: str) -> List[str]: ...
def urlpathsplit(url: AnyUrlTarget) -> List[str]: ...
def normpath(urlpath: str, drop_consecutive_slashes: bool = True) -> str: ...
def attempt_to_decode_idna(string: str) -> str: ...
@overload
def decode_punycode_hostname(hostname: str, as_parts: Literal[False] = ...) -> str: ...
@overload
def decode_punycode_hostname(
    hostname: str, as_parts: Literal[True] = ...
) -> List[str]: ...
def fix_common_query_mistakes(query: str) -> str: ...
def safe_parse_qs(query: str) -> Dict[str, List[str]]: ...
def add_query_argument(
    url: str, name: str, value: QueryArgValue, quote: bool = ...
) -> str: ...
