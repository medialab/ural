# =============================================================================
# Ural LRUTrie Classes
# =============================================================================
#
# Bunch of classes relying on LRUs and prefix trees to perform complex URL
# matching routines.
#
from phylactery import TrieDict
from ural.lru import normalized_lru_stems, lru_stems
from functools import partial


class LRUTrie(TrieDict):
    def set(self, url, metadata):
        stems = lru_stems(url)
        super(LRUTrie, self).set(stems, metadata)

    def match(self, url):
        stems = lru_stems(url)
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
