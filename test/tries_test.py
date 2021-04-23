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
        trie.add('LACAMARGUE.net')

        assert len(trie) == 3

        assert not trie.match('https://lefigaro.fr/article1.html')
        assert not trie.match('http://localhost:8000')
        assert not trie.match('https://192.168.0.1')
        assert trie.match('https://lemonde.fr/article1.html')
        assert trie.match('https://business.lemonde.fr/article1.html')
        assert not trie.match('https://google.com/article1.html')
        assert trie.match('https://feedproxy.google.com/article1.html')
        assert trie.match('https://www.LACAMARGUE.net/article1.html')
        assert trie.match('https://www.lacamargue.net/article1.html')

        assert set(trie) == {
            'lemonde.fr',
            'feedproxy.google.com',
            'lacamargue.net'
        }
