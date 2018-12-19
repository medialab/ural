#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Simple LRU Unit Tests
# =============================================================================
from ural import simple_lru

DEFAULT_TESTS = [
    ('http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2',
     ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'q:query=mobile']),
    ('http://www.example.com/wpstyle/?p=364&q=365',
     ['s:http', 'h:com', 'h:example', 'h:www', 'p:wpstyle', 'q:p=364', 'q:q=365']),
    ('www.foo.bar/index.html', ['h:bar', 'h:foo', 'h:www'])
]


class TestIsUrl(object):
    def test_basics(self):
        for url, lru in DEFAULT_TESTS:
            assert simple_lru(url) == lru
