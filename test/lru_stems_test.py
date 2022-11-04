#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural LRU Stems Unit Tests
# =============================================================================
from ural.lru import lru_stems

DEFAULT_TESTS = [
    (
        "http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2",
        [
            "s:http",
            "t:8000",
            "h:fr",
            "h:lemonde",
            "h:www",
            "p:article",
            "p:1234",
            "p:index.html",
            "q:query=mobile",
            "f:2",
        ],
    ),
    (
        "http://www.example.com/wpstyle/?p=364&q=365&a=284#anchor",
        [
            "s:http",
            "h:com",
            "h:example",
            "h:www",
            "p:wpstyle",
            "p:",
            "q:p=364&q=365&a=284",
            "f:anchor",
        ],
    ),
    ("www.foo.bar/index.html", ["s:http", "h:bar", "h:foo", "h:www", "p:index.html"]),
    ("site.com/page/", ["s:http", "h:com", "h:site", "p:page", "p:"]),
    ("site.com?", ["s:http", "h:com", "h:site"]),
    ("http://user@lemonde.fr", ["s:http", "h:fr", "h:lemonde", "u:user"]),
    ("http://user:mdp@lemonde.fr", ["s:http", "h:fr", "h:lemonde", "u:user", "w:mdp"]),
    ("http://theguardian.co.uk", ["s:http", "h:uk", "h:co", "h:theguardian"]),
    # ('http://theguardian.co.uk/path?', ['s:http', 'h:uk', 'h:co', 'h:theguardian', 'p:path', 'q:']),
    # ('http://theguardian.co.uk/path#', ['s:http', 'h:uk', 'h:co', 'h:theguardian', 'p:path', 'f:']),
    # ('http://theguardian.co.uk/path?#', ['s:http', 'h:uk', 'h:co', 'h:theguardian', 'p:path', 'q:', 'f:']),
    ("http://cuts.An", ["s:http", "h:An", "h:cuts"]),
    ("http://black.bl", ["s:http", "h:bl", "h:black"]),
    ("http://[2001:4860:0:2001::68]/", ["s:http", "h:[2001:4860:0:2001::68]", "p:"]),
    ("http://192.14.253.56/hello.html", ["s:http", "h:192.14.253.56", "p:hello.html"]),
    (
        "http://localhost:443/hello.html",
        ["s:http", "t:443", "h:localhost", "p:hello.html"],
    ),
]

TLD_AWARE_TESTS = [
    ("http://theguardian.co.uk", ["s:http", "h:co.uk", "h:theguardian"]),
    (
        "http://user:mdp@lemonde.co.uk",
        ["s:http", "h:co.uk", "h:lemonde", "u:user", "w:mdp"],
    ),
    (
        "http://www.example.com/wpstyle/?p=364&q=365&a=284#anchor",
        [
            "s:http",
            "h:com",
            "h:example",
            "h:www",
            "p:wpstyle",
            "p:",
            "q:p=364&q=365&a=284",
            "f:anchor",
        ],
    ),
    (
        "http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2",
        [
            "s:http",
            "t:8000",
            "h:fr",
            "h:lemonde",
            "h:www",
            "p:article",
            "p:1234",
            "p:index.html",
            "q:query=mobile",
            "f:2",
        ],
    ),
    ("https://www.lemonde.frcom", ["s:https", "h:frcom", "h:lemonde", "h:www"]),
    (
        "https://www.courrierinternational.compage",
        ["s:https", "h:compage", "h:courrierinternational", "h:www"],
    ),
    ("http://cuts.An", ["s:http", "h:An", "h:cuts"]),
    ("http://black.bl", ["s:http", "h:bl", "h:black"]),
    ("http://[2001:4860:0:2001::68]/", ["s:http", "h:[2001:4860:0:2001::68]", "p:"]),
    ("http://192.14.253.56/hello.html", ["s:http", "h:192.14.253.56", "p:hello.html"]),
    (
        "http://localhost:443/hello.html",
        ["s:http", "t:443", "h:localhost", "p:hello.html"],
    ),
]


class TestLruStems(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert lru_stems(url, tld_aware=False) == result
        for url, result in TLD_AWARE_TESTS:
            assert lru_stems(url, tld_aware=True) == result, url
