from typing import Optional, Iterator, Union

def urls_from_html(
    html: Union[bytes, str],
    encoding: str = ...,
    errors: str = ...,
) -> Iterator[str]: ...
