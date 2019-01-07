#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRU Unit Tests
# =============================================================================
from ural import lru

DEFAULT_TESTS = [
    ('http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2',
     ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html', 'q:query=mobile', 'f:2']),
    ('http://www.example.com/wpstyle/?p=364&q=365&a=284#anchor',
     ['s:http', 'h:com', 'h:example', 'h:www', 'p:wpstyle', 'p:', 'q:p=364&q=365&a=284', 'f:anchor']),
    ('www.foo.bar/index.html', ['s:http',
                                'h:bar', 'h:foo', 'h:www', 'p:index.html']),
    ('site.com/page/', ['s:http', 'h:com', 'h:site', 'p:page', 'p:'])
]


class TestIsUrl(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert lru(url) == result
