# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from phylactery import TrieDict
from functools import partial

from ural.utils import string_type
from ural.lru.stems import normalized_lru_stems, lru_stems
from ural.lru.serialization import unserialize_lru


def ensure_lru_stems(lru):
    if isinstance(lru, string_type):
        return unserialize_lru(lru)

    return lru


class LRUTrie(TrieDict):
    def __init__(self, tld_aware=False):
        super(LRUTrie, self).__init__(list)
        self.__lru_stems = partial(lru_stems, tld_aware=tld_aware)

    def set(self, url, metadata):
        stems = self.__lru_stems(url)
        super(LRUTrie, self).set(stems, metadata)

    def match(self, url):
        stems = self.__lru_stems(url)
        return self.longest(stems)

    def set_lru(self, lru, metadata):
        stems = ensure_lru_stems(lru)
        super(LRUTrie, self).set(stems, metadata)

    def match_lru(self, lru):
        stems = ensure_lru_stems(lru)
        return self.longest(stems)

    def __iter__(sefl):
        return self.values()


class NormalizedLRUTrie(TrieDict):
    def __init__(self, **kwargs):
        super(NormalizedLRUTrie, self).__init__()
        self.normalize = partial(normalized_lru_stems, **kwargs)

    def set(self, url, metadata):
        stems = self.normalize(url)
        super(NormalizedLRUTrie, self).set(stems, metadata)

    def match(self, url):
        stems = self.normalize(url)
        return self.longest(stems)

    def __iter__(self):
        return self.values()
