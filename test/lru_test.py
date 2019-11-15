#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRU Unit Tests
# =============================================================================
from ural.lru import url_to_lru

TESTS = [
    ('http://www.lemonde.fr/articles/summary.html', 's:http|h:fr|h:lemonde|h:www|p:articles|p:summary.html|')
]


class TestLru(object):
    def test_url_to_lru(self):
        for url, lru in TESTS:
            assert url_to_lru(url) == lru
