# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from functools import partial

from ural.classes import TrieDict
from ural.utils import string_type
from ural.lru.stems import normalized_lru_stems, lru_stems
from ural.lru.serialization import unserialize_lru


def ensure_lru_stems(lru):
    if isinstance(lru, string_type):
        return unserialize_lru(lru)

    return lru


def clean_trailing_path(stems):
    return [stem for stem in stems if stem != "p:"]


class LRUTrie(object):
    def __init__(self, suffix_aware=False):
        self._trie = TrieDict()
        self.lru_tokenizer = partial(lru_stems, suffix_aware=suffix_aware)

    def __len__(self):
        return len(self._trie)

    def set(self, url, metadata):
        stems = self.lru_tokenizer(url)
        stems = clean_trailing_path(stems)
        self._trie[stems] = metadata

    def __setitem__(self, url, metadata):
        return self.set(url, metadata)

    def match(self, url):
        stems = self.lru_tokenizer(url)
        stems = clean_trailing_path(stems)
        return self._trie.longest_matching_prefix_value(stems)

    def set_lru(self, lru, metadata):
        stems = ensure_lru_stems(lru)
        stems = clean_trailing_path(stems)
        self._trie[stems] = metadata

    def match_lru(self, lru):
        stems = ensure_lru_stems(lru)
        stems = clean_trailing_path(stems)
        return self._trie.longest_matching_prefix_value(stems)

    def __iter__(self):
        return self._trie.values()


class NormalizedLRUTrie(LRUTrie):
    def __init__(self, suffix_aware=False, **kwargs):
        self._trie = TrieDict()
        self.lru_tokenizer = partial(
            normalized_lru_stems, suffix_aware=suffix_aware, **kwargs
        )
