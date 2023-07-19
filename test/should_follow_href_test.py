#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Follow Href Unit Tests
# =============================================================================
from ural.should_follow_href import should_follow_href

TESTS = [
    ("#top", False),
    ("  #strip", False),
    ("magnet:uri-xIOhoug", False),
    ("home.html", True),
    ("/home.html", True),
    ("./home.html", True),
    ("https://www.lemonde.fr", True),
    ('HTTP://www.lemonde.fr', True),
    ('http:www.lemonde', False),
    ("mailto:whatever@gmail.com", False),
    ("tel:053775175743", False),
    ('javascript:alert("hello")', False),
    ("file:///home/test/ok", False),
    ("ftp:whatever", False),
    ("", False),
]


class TestShouldFollowHref(object):
    def test_basics(self):
        for href, result in TESTS:
            assert should_follow_href(href) == result, href
