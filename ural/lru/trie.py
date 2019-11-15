# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from phylactery import TrieDict
from functools import partial

from ural.lru.stems import normalized_lru_stems, lru_stems
from ural.lru.serialization import unserialize_lru

# PY2/PY3 compatible string_type...
string_type = str

try:
    string_type = basestring
except NameError:
    pass


def ensure_lru_stems(lru):
    if isinstance(lru, string_type):
        return unserialize_lru(lru)

    return lru


class LRUTrie(TrieDict):
    def set(self, url, metadata):
        stems = lru_stems(url)
        super(LRUTrie, self).set(stems, metadata)

    def match(self, url):
        stems = lru_stems(url)
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
