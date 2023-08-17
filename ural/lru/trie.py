# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from ural.classes import TrieDict
from ural.utils import string_type
from ural.lru.stems import (
    lru_stems,
    canonicalized_lru_stems,
    normalized_lru_stems,
    fingerprinted_lru_stems,
)
from ural.lru.serialization import unserialize_lru


def ensure_lru_stems(lru):
    if isinstance(lru, string_type):
        return unserialize_lru(lru)

    return lru


def clean_trailing_path(stems):
    return [stem for stem in stems if stem != "p:"]


class LRUTrie(object):
    def __init__(self, suffix_aware=False, **kwargs):
        self.__trie = TrieDict()
        self.kwargs = kwargs
        self.suffix_aware = suffix_aware

    def tokenize(self, url):
        return lru_stems(url, suffix_aware=self.suffix_aware)

    def __len__(self):
        return len(self.__trie)

    def set(self, url, metadata):
        stems = self.tokenize(url)
        stems = clean_trailing_path(stems)
        self.__trie[stems] = metadata

    def __setitem__(self, url, metadata):
        return self.set(url, metadata)

    def match(self, url):
        stems = self.tokenize(url)
        stems = clean_trailing_path(stems)
        return self.__trie.longest_matching_prefix_value(stems)

    def set_lru(self, lru, metadata):
        stems = ensure_lru_stems(lru)
        stems = clean_trailing_path(stems)
        self.__trie[stems] = metadata

    def match_lru(self, lru):
        stems = ensure_lru_stems(lru)
        stems = clean_trailing_path(stems)
        return self.__trie.longest_matching_prefix_value(stems)

    def __iter__(self):
        return self.__trie.values()


class CanonicalizedLRUTrie(LRUTrie):
    def tokenize(self, url):
        return canonicalized_lru_stems(
            url, suffix_aware=self.suffix_aware, **self.kwargs
        )


class NormalizedLRUTrie(LRUTrie):
    def tokenize(self, url):
        return normalized_lru_stems(url, suffix_aware=self.suffix_aware, **self.kwargs)


class FingerprintedLRUTrie(LRUTrie):
    def tokenize(self, url):
        return fingerprinted_lru_stems(
            url, suffix_aware=self.suffix_aware, **self.kwargs
        )
