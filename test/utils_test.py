#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Utils Unit Tests
# =============================================================================
from ural.utils import urlpathsplit

URLPATHSPLIT_TESTS = [
    ("", []),
    ("/", []),
    ("/path", ["path"]),
    ("/path/", ["path"]),
    ("/very/long/path/with/trailing/", ["very", "long", "path", "with", "trailing"]),
]


class TestUtils(object):
    def test_urlpathsplit(self):
        for path, result in URLPATHSPLIT_TESTS:
            assert urlpathsplit(path) == result
