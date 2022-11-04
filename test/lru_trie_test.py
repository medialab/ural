#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRUTrie Unit Tests
# =============================================================================
from ural.lru import LRUTrie, NormalizedLRUTrie


class TestNormalizedLRUTrie(object):
    def test_lru_trie(self):
        trie = LRUTrie()

        trie.set("http://lemonde.fr", 1)
        trie.set("http://lemonde.fr/articles/economy", 2)

        assert len(trie) == 2

        assert list(trie) == [1, 2]

        assert trie.match("http://lefigaro.fr") is None
        assert trie.match("http://lemonde.fr/categories/whatever") == 1
        assert trie.match("http://lemonde.fr/articles/economy/index.html") == 2

        trie.set_lru(["s:http", "h:fr", "h:lefigaro"], 3)
        trie.set_lru("s:http|h:fr|h:lefigaro|p:articles|p:whatever.html|", 4)

        assert len(trie) == 4

        assert trie.match_lru(["s:http", "h:fr", "h:lefigaro", "p:test"]) == 3
        assert trie.match_lru("s:http|h:fr|h:lefigaro|p:articles|p:whatever.html|") == 4

    def test_normalized_lru_trie(self):
        trie = NormalizedLRUTrie()
        trie.set("http://www.lemonde.fr", {"media": "lemonde"})
        trie.set(
            "http://www.lemonde.fr/politique/article",
            {"media": "lemonde", "type": "article"},
        )
        assert trie.match("http://www.lemonde.fr") == {"media": "lemonde"}
        assert trie.match("http://www.lemonde.fr/politique/") == {"media": "lemonde"}
        assert trie.match("http://www.lemonde.fr/politique/article") == {
            "media": "lemonde",
            "type": "article",
        }
        assert trie.match("http://www.lemonde.fr/politique/article/randompath") == {
            "media": "lemonde",
            "type": "article",
        }
        assert trie.match("http://www.legorafi.fr") is None

        assert len(trie) == 2

        assert list(trie) == [
            {"media": "lemonde"},
            {"media": "lemonde", "type": "article"},
        ]

    def test_edge_cases(self):
        trie = LRUTrie()

        assert (
            trie.match(
                "http://127.0.0.1/economie/2019/01/08/un-journaliste-poursuit-richard-ferrand-pour-lavoir-bloque-sur-twitter/"
            )
            is None
        )

    def test_trailing_path(self):
        trie = LRUTrie()

        trie.set("http://www.zejournal.mobi/", "Ze Journal mobi")

        assert (
            trie.match("http://www.zejournal.mobi/id/news/show_detail/14853")
            == "Ze Journal mobi"
        )
