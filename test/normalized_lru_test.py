#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Normalized LRU from URL Unit Tests
# =============================================================================
from ural import normalized_lru_from_url

DEFAULT_TESTS = [
    ('http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2',
     ['t:8000', 'h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:query=mobile']),
    ('http://www.example.com/wpstyle/?p=364&q=365',
     ['h:com', 'h:example', 'p:wpstyle', 'p:', 'q:p=364&q=365']),
    ('www.foo.bar/index.html', ['h:bar', 'h:foo'])
]


class TestIsUrl(object):
    def test_basics(self):
        for url, lru in DEFAULT_TESTS:
            assert normalized_lru_from_url(url) == lru
        assert normalized_lru_from_url('www.foo.bar/index.html',
                                       strip_index=False) == ['h:bar', 'h:foo', 'p:index.html']
        assert normalized_lru_from_url('http://www.foo.bar/index.html',
                                       strip_protocol=False) == ['s:http', 'h:bar', 'h:foo']
