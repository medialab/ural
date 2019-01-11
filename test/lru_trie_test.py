#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRUTrie Unit Tests
# =============================================================================
from ural import LRUTrie


class TestIsUrl(object):
    def test_basics(self):
        trie = LRUTrie()
        trie.set('http://www.lemonde.fr', {'media': 'lemonde'})
        assert trie.match('http://www.lemonde.fr') == {'media': 'lemonde'}
