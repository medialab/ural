#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRU Unit Tests
# =============================================================================
from ural.lru import url_to_lru, lru_to_url

TESTS = [
    ('http://www.lemonde.fr/articles/summary.html', 's:http|h:fr|h:lemonde|h:www|p:articles|p:summary.html|'),
    ('http://user:mdp@www.lemonde.fr:4000/articles/summary.html?query=ok#fragment', 's:http|t:4000|h:fr|h:lemonde|h:www|p:articles|p:summary.html|q:query=ok|f:fragment|u:user|w:mdp|'),
    # ('http://lemonde.fr?', 's:http|h:fr|h:lemonde|q:|')
]


class TestLru(object):
    def test_url_to_lru(self):
        for url, lru in TESTS:
            assert url_to_lru(url) == lru

    def test_lru_to_url(self):
        for url, lru in TESTS:
            assert lru_to_url(lru) == url

    def test_idempotency(self):
        for url, lru in TESTS:
            assert url_to_lru(lru_to_url(lru)) == lru
            assert lru_to_url(url_to_lru(url)) == url
