# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Trie Set Unit Tests
# =============================================================================
from ural import HostnameTrieSet


class TestHostnameTrieSet(object):
    def test_basics(self):
        trie = HostnameTrieSet()

        trie.add('lemonde.fr')
        trie.add('business.lemonde.fr')
        trie.add('feedproxy.google.com')
        trie.add('LACAMARGUE.net')
        trie.add('2001:4860:0:2001::68')

        assert len(trie) == 4

        assert not trie.match('https://lefigaro.fr/article1.html')
        assert not trie.match('http://localhost:8000')
        assert not trie.match('https://192.168.0.1')
        assert trie.match('https://lemonde.fr/article1.html')
        assert trie.match('https://business.lemonde.fr/article1.html')
        assert not trie.match('https://google.com/article1.html')
        assert trie.match('https://feedproxy.google.com/article1.html')
        assert trie.match('https://www.LACAMARGUE.net/article1.html')
        assert trie.match('https://www.lacamargue.net/article1.html')
        assert trie.match('https://[2001:4860:0:2001::68]')

        assert set(trie) == {
            '2001:4860:0:2001::68',
            'lemonde.fr',
            'feedproxy.google.com',
            'lacamargue.net',
        }

        trie.add('xn--tlrama-bvab.fr')

        assert len(trie) == 5

        assert trie.match('xn--tlrama-bvab.fr')
        assert trie.match(u'télérama.fr')

        assert set(trie) == {
            'lemonde.fr',
            'feedproxy.google.com',
            'lacamargue.net',
            u'télérama.fr',
            '2001:4860:0:2001::68'
        }
