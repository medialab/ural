# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Trie Set Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural import HostnameTrieSet


class TestHostnameTrieSet(object):
    def test_basics(self):
        trie = HostnameTrieSet()

        trie.add("feedproxy.google.com")
        trie.add("LACAMARGUE.net")
        trie.add("2001:4860:0:2001::68")
        trie.add("busIness.leMONde.fr")
        trie.add("home.lemonde.fr")

        assert len(trie) == 5

        assert not trie.match("https://lefigaro.fr/article1.html")
        assert not trie.match("http://localhost:8000")
        assert not trie.match("https://192.168.0.1")
        assert trie.match("https://business.lemonde.fr/article1.html")
        assert trie.match("https://home.lemonde.fr/article1.html")
        assert not trie.match("https://lemonde.fr/article1.html")
        assert not trie.match("https://google.com/article1.html")
        assert trie.match("https://feedproxy.google.com/article1.html")
        assert trie.match("https://www.LACAMARGUE.net/article1.html")
        assert trie.match("https://www.lacamargue.net/article1.html")
        assert trie.match("https://[2001:4860:0:2001::68]")

        assert set(trie) == {
            "2001:4860:0:2001::68",
            "business.lemonde.fr",
            "home.lemonde.fr",
            "feedproxy.google.com",
            "lacamargue.net",
        }

        trie.add("xN--tlrama-bvAb.fr")
        trie.add("xn--tlrama-bvab.fr")
        trie.add("lemonde.fr")

        assert len(trie) == 5

        trie.add("social.lemonde.fr")

        assert len(trie) == 5

        assert trie.match("xn--tlrama-bvab.fr")
        assert trie.match("télérama.fr")
        assert trie.match("https://business.lemonde.fr/article1.html")
        assert trie.match("https://lemonde.fr/article1.html")
        assert trie.match("https://social.lemonde.fr/article1.html")

        assert set(trie) == {
            "lemonde.fr",
            "feedproxy.google.com",
            "lacamargue.net",
            "télérama.fr",
            "2001:4860:0:2001::68",
        }
