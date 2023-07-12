from typing import Union, overload
from ural.types import AnyUrlTarget, Literal
from urllib.parse import SplitResult

@overload
def normalize_url(
    url: AnyUrlTarget,
    unsplit: Literal[False] = ...,
    sort_query: bool = ...,
    strip_authentication: bool = ...,
    strip_trailing_slash: bool = ...,
    strip_index: bool = ...,
    strip_protocol: bool = ...,
    strip_irrelevant_subdomains: bool = ...,
    strip_lang_subdomains: bool = ...,
    strip_lang_query_items: bool = ...,
    strip_fragment: Union[bool, Literal["except-routing"]] = ...,
    normalize_amp: bool = ...,
    fix_common_mistakes: bool = ...,
    infer_redirection: bool = ...,
    quoted: bool = ...,
) -> str: ...
@overload
def normalize_url(
    url: AnyUrlTarget,
    unsplit: Literal[True] = ...,
    sort_query: bool = ...,
    strip_authentication: bool = ...,
    strip_trailing_slash: bool = ...,
    strip_index: bool = ...,
    strip_protocol: bool = ...,
    strip_irrelevant_subdomains: bool = ...,
    strip_lang_subdomains: bool = ...,
    strip_lang_query_items: bool = ...,
    strip_fragment: Union[bool, Literal["except-routing"]] = ...,
    normalize_amp: bool = ...,
    fix_common_mistakes: bool = ...,
    infer_redirection: bool = ...,
    quoted: bool = ...,
) -> SplitResult: ...
def normalize_hostname(
    hostname: str, normalize_amp: bool = True, strip_lang_subdomains: bool = False
) -> str: ...
def get_normalized_hostname(
    url: AnyUrlTarget,
    normalize_amp: bool = True,
    strip_lang_subdomains: bool = False,
    infer_redirection: bool = True,
) -> str: ...
