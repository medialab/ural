#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRUTrie Unit Tests
# =============================================================================
from ural import LRUTrie


class TestLRUTrie(object):
    def test_basics(self):
        trie = LRUTrie()
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
