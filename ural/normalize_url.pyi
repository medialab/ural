from typing import Union, Optional, Callable, overload
from ural.types import AnyUrlTarget, Literal
from urllib.parse import SplitResult

@overload
def normalize_url(
    url: str,
    unsplit: Literal[False] = ...,
    sort_query: bool = ...,
    strip_authentication: bool = ...,
    strip_trailing_slash: bool = ...,
    strip_index: bool = ...,
    strip_protocol: bool = ...,
    strip_irrelevant_subdomains: bool = ...,
    strip_fragment: Union[bool, Literal["except-routing"]] = ...,
    query_item_filter: Optional[Callable[[str, str], bool]] = ...,
    normalize_amp: bool = ...,
    fix_common_mistakes: bool = ...,
    infer_redirection: bool = ...,
    quoted: bool = ...,
) -> SplitResult: ...
@overload
def normalize_url(
    url: str,
    unsplit: Literal[True] = ...,
    sort_query: bool = ...,
    strip_authentication: bool = ...,
    strip_trailing_slash: bool = ...,
    strip_index: bool = ...,
    strip_protocol: bool = ...,
    strip_irrelevant_subdomains: bool = ...,
    strip_fragment: Union[bool, Literal["except-routing"]] = ...,
    query_item_filter: Optional[Callable[[str, str], bool]] = ...,
    normalize_amp: bool = ...,
    fix_common_mistakes: bool = ...,
    infer_redirection: bool = ...,
    quoted: bool = ...,
) -> str: ...
def normalize_hostname(hostname: str, normalize_amp: bool = True) -> str: ...
def get_normalized_hostname(
    url: AnyUrlTarget,
    normalize_amp: bool = True,
    infer_redirection: bool = True,
) -> str: ...
