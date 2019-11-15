#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRUTrie Unit Tests
# =============================================================================
from ural.lru import NormalizedLRUTrie


class TestNormalizedLRUTrie(object):
    def test_basics(self):
        trie = NormalizedLRUTrie()
        trie.set('http://www.lemonde.fr', {'media': 'lemonde'})
        trie.set('http://www.lemonde.fr/politique/article',
                 {'media': 'lemonde', 'type': 'article'})
        assert trie.match('http://www.lemonde.fr') == {'media': 'lemonde'}
        assert trie.match(
            'http://www.lemonde.fr/politique/') == {'media': 'lemonde'}
        assert trie.match(
            'http://www.lemonde.fr/politique/article') == {'media': 'lemonde', 'type': 'article'}
        assert trie.match(
            'http://www.lemonde.fr/politique/article/randompath') == {'media': 'lemonde', 'type': 'article'}
        assert trie.match('http://www.legorafi.fr') is None

        assert len(trie) == 2

        assert list(trie) == [
            {'media': 'lemonde'},
            {'media': 'lemonde', 'type': 'article'}
        ]
