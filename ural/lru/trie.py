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


class NormalizedLRUTrie(TrieDict):
    def __init__(self, **kwargs):
        super(NormalizedLRUTrie, self).__init__()
        self.normalize = partial(normalized_lru_stems, **kwargs)

    def set(self, url, metadata):
        lru = self.normalize(url)
        super(NormalizedLRUTrie, self).set(lru, metadata)

    def match(self, url):
        lru = self.normalize(url)
        return self.longest(lru)

    def __iter__(self):
        return self.values()
