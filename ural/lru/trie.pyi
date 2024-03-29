# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from typing import Generic, TypeVar, Optional, List, Iterator

Metadata = TypeVar("Metadata")

class LRUTrie(Generic[Metadata]):
    def __init__(self, suffix_aware: bool = ..., **kwargs): ...
    def __len__(self) -> int: ...
    def set(self, url: str, metadata: Metadata) -> None: ...
    def __setitem__(self, url: str, metadata: Metadata) -> None: ...
    def match(self, url: str) -> Optional[Metadata]: ...
    def set_lru(self, lru: List[str], metadata: Metadata): ...
    def match_lru(self, lru: List[str]) -> Optional[Metadata]: ...
    def __iter__(self) -> Iterator[Metadata]: ...

class CanonicalizedLRUTrie(LRUTrie[Metadata]):
    pass

class NormalizedLRUTrie(LRUTrie[Metadata]):
    pass

class FingerprintedLRUTrie(LRUTrie[Metadata]):
    pass
