from typing import List
from urllib.parse import SplitResult

def lru_stems_from_parsed_url(
    parsed_url: SplitResult, suffix_aware: bool = ...
) -> List[str]: ...
def lru_stems(url: str, suffix_aware: bool = ...): ...
def canonicalized_lru_stems(url: str, suffix_aware: bool = ..., **kwargs): ...
def normalized_lru_stems(url: str, suffix_aware: bool = ..., **kwargs): ...
def fingerprinted_lru_stems(url: str, suffix_aware: bool = ..., **kwargs): ...
