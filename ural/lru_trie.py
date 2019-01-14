# =============================================================================
# Ural LRUTrie class
# =============================================================================
#
# A class implementing a prefix tree(Trie) storing LRUs and their metadata,
# allowing to find the longest common prefix between two urls.
#
from phylactery import TrieDict
from ural.normalized_lru_from_url import normalized_lru_from_url
from functools import partial


class LRUTrie(object):
    def __init__(self, **kwargs):
        self.trie = TrieDict()
        self.normalize = partial(normalized_lru_from_url, **kwargs)

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
