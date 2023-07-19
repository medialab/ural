#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Link Extraction From HTML Unit Tests
# =============================================================================
from __future__ import unicode_literals
from ural import links_from_html

LINKS_TESTS = b"""
<div>
    <a href="javascript:alert('hello');">click</a>
    <a href="http://lemonde.fr">lemonde</a>
    <a href="http://lemonde.fr">lemonde</a>
    <a href="http://lemonde.fr#test">lemonde</a>
    <a href="HTTP://LEMONDE.FR">lemonde</a>
    <a href="HTTP://LEMONDE.idontexistlol">lemonde</a>
    <a href="article.html">lemonde</a>
</div>
"""


class TestLinksFromHtml(object):
    def test_basics(self):
        assert list(links_from_html("http://lefigaro.fr", LINKS_TESTS)) == [
            "http://lemonde.fr",
            "http://lemonde.fr",
            "http://lemonde.fr#test",
            "HTTP://LEMONDE.FR",
            "http://lefigaro.fr/article.html",
        ]

        assert list(links_from_html("http://lemonde.fr", LINKS_TESTS)) == [
            "http://lemonde.fr#test",
            "HTTP://LEMONDE.FR",
            "http://lemonde.fr/article.html",
        ]

        assert list(
            links_from_html(
                "http://lemonde.fr", LINKS_TESTS, canonicalize=True, strip_fragment=True
            )
        ) == ["http://lemonde.fr/article.html"]

        assert list(
            links_from_html("http://lefigaro.fr", LINKS_TESTS, canonicalize=True)
        ) == [
            "http://lemonde.fr",
            "http://lemonde.fr",
            "http://lemonde.fr/#test",
            "http://lemonde.fr",
            "http://lefigaro.fr/article.html",
        ]

        assert list(
            links_from_html(
                "http://lefigaro.fr", LINKS_TESTS, canonicalize=True, unique=True
            )
        ) == [
            "http://lemonde.fr",
            "http://lemonde.fr/#test",
            "http://lefigaro.fr/article.html",
        ]

        assert list(
            links_from_html(
                "http://lefigaro.fr",
                LINKS_TESTS,
                canonicalize=True,
                unique=True,
                strip_fragment=True,
            )
        ) == [
            "http://lemonde.fr",
            "http://lefigaro.fr/article.html",
        ]
