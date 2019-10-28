# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from phylactery import TrieDict
from ural.lru import normalized_lru_stems
from functools import partial


class NormalizedLRUTrie(object):
    def __init__(self, **kwargs):
        self.trie = TrieDict()
        self.normalize = partial(normalized_lru_stems, **kwargs)

    def set(self, url, metadata):
        lru = self.normalize(url)
        self.trie.set(lru, metadata)

    def match(self, url):
        lru = self.normalize(url)
        return self.trie.longest(lru)

    def values(self):
        return self.trie.values()

    def __iter__(self):
        return self.trie.values()
