# =============================================================================
# Ural Tries Unit Tests
# =============================================================================
from ural import HostnameTrieSet


class TestTries(object):
    def test_hostname_trie_set(self):
        trie = HostnameTrieSet()

        trie.add('lemonde.fr')
        trie.add('business.lemonde.fr')
        trie.add('feedproxy.google.com')

        assert len(trie) == 2

        assert not trie.match_url('https://lefigaro.fr/article1.html')
        assert not trie.match_url('http://localhost:8000')
        assert not trie.match_url('https://192.168.0.1')
        assert trie.match_url('https://lemonde.fr/article1.html')
        assert trie.match_url('https://business.lemonde.fr/article1.html')
        assert not trie.match_url('https://google.com/article1.html')
        assert trie.match_url('https://feedproxy.google.com/article1.html')
