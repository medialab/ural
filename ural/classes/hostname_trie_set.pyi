from typing import Iterator
from ural.types import AnyUrlTarget

class HostnameTrieSet(object):
    def __len__(self) -> int: ...
    def add(self, hostname: str) -> None: ...
    def match(self, url: AnyUrlTarget) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __contains__(self, hostname: str) -> None: ...
