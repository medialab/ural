#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Utils Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural.utils import (
    pathsplit,
    urlpathsplit,
    decode_punycode_hostname,
    safe_urlsplit,
    add_get_param,
)

PATHSPLIT_TESTS = [
    ("", []),
    ("/", []),
    ("/path", ["path"]),
    ("/path/", ["path"]),
    ("/very/long/path/with/trailing/", ["very", "long", "path", "with", "trailing"]),
]


class TestUtils(object):
    def test_pathsplit(self):
        for path, result in PATHSPLIT_TESTS:
            assert pathsplit(path) == result

    def test_urlpathsplit(self):
        assert urlpathsplit("http://lemonde.fr/article.html") == ["article.html"]
        assert urlpathsplit("http://lemonde.fr") == []
        assert urlpathsplit(safe_urlsplit("http://lemonde.fr/")) == []

    def test_decode_punycode_hostname(self):
        assert decode_punycode_hostname("xn--tlrama-bvab.fr") == "télérama.fr"
        assert decode_punycode_hostname("xn--tlraMA-bvab.fr") == "téléraMA.fr"
        assert (
            decode_punycode_hostname("business.xn--tlrama-bvab.fr")
            == "business.télérama.fr"
        )
        assert decode_punycode_hostname("xN--tlrama-bvab.fr") == "télérama.fr"

    def test_add_get_param(self):
        assert add_get_param("http://lemonde.fr", "test") == "http://lemonde.fr?test"
        assert (
            add_get_param("http://lemonde.fr", "test", "val")
            == "http://lemonde.fr?test=val"
        )
        assert (
            add_get_param("http://lemonde.fr#anchor", "test", "val")
            == "http://lemonde.fr?test=val#anchor"
        )
        assert (
            add_get_param("http://lemonde.fr?hello=world#anchor", "test", "val")
            == "http://lemonde.fr?hello=world&test=val#anchor"
        )
        assert (
            add_get_param("http://lemonde.fr?hello=world", "test", "val")
            == "http://lemonde.fr?hello=world&test=val"
        )
        assert (
            add_get_param("http://lemonde.fr?hello=world&one=two", "test", "val")
            == "http://lemonde.fr?hello=world&one=two&test=val"
        )
        assert (
            add_get_param("http://lemonde.fr?hello&one=two", "test", "val")
            == "http://lemonde.fr?hello&one=two&test=val"
        )
        assert add_get_param("lemonde.fr", "test", "val") == "lemonde.fr?test=val"
        assert add_get_param("lemonde.fr", "test", 45) == "lemonde.fr?test=45"
