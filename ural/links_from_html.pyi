from typing import Iterator, Union

def links_from_html(
    base_url: str,
    html_body: Union[bytes, str],
    encoding: str = ...,
    canonicalize: bool = ...,
    unique: bool = ...,
    strip_fragment: bool = ...,
) -> Iterator[str]: ...
