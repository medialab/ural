from typing import Optional, Iterator, Union

def urls_from_html(
    html: Union[bytes, str],
    base_url: Optional[str] = ...,
    encoding: str = ...,
    errors: str = ...,
) -> Iterator[str]: ...
