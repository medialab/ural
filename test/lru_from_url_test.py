#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRU from URL Unit Tests
# =============================================================================
from ural import lru_from_url

DEFAULT_TESTS = [
    ('http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2',
     ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html', 'q:query=mobile', 'f:2']),
    ('http://www.example.com/wpstyle/?p=364&q=365&a=284#anchor',
     ['s:http', 'h:com', 'h:example', 'h:www', 'p:wpstyle', 'p:', 'q:p=364&q=365&a=284', 'f:anchor']),
    ('www.foo.bar/index.html', ['s:http',
                                'h:bar', 'h:foo', 'h:www', 'p:index.html']),
    ('site.com/page/', ['s:http', 'h:com', 'h:site', 'p:page', 'p:']),
    ('site.com?', ['s:http', 'h:com', 'h:site']),
    ('http://user@lemonde.fr', ['s:http', 'h:fr', 'h:lemonde', 'u:user']),
    ('http://user:mdp@lemonde.fr', ['s:http', 'h:fr', 'h:lemonde', 'u:user', 'w:mdp']),
    ('http://theguardian.co.uk', ['s:http', 'h:uk', 'h:co', 'h:theguardian'])
]

TLD_AWARE_TESTS = [
    ('http://theguardian.co.uk', ['s:http', 'h:co.uk', 'h:theguardian'])
]


class TestIsUrl(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert lru_from_url(url) == result
