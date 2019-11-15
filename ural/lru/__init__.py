# =============================================================================
# Ural LRU Module
# =============================================================================
#
# Module gathering LRU-related functions.
#
from ural.lru.serialization import serialize_lru, unserialize_lru
from ural.lru.stems import lru_stems, normalized_lru_stems
from ural.lru.trie import LRUTrie, NormalizedLRUTrie


def url_to_lru(url, tld_aware=False):
    return serialize_lru(lru_stems(url, tld_aware=tld_aware))
