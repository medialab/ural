#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Has Special Host Unit Tests
# =============================================================================
from ural import has_special_host, is_special_host

TESTS_IS = [
    ("127.0.0.1", True),
    ("youtube.com", False),
    ("104.19.154.83", True),
    ("192.14.253.56", True),
    ("localhost:443", True),
    ("localhost", True),
    ("2601:19b:700:b70:1106:49ab:ac46:2e12", True),
    ("2001:4860:0:2001::68", True),
    ("::1", True),
]

TESTS_HAS = [
    ("http://127.0.0.1", True),
    ("http://youtube.com", False),
    ("http://104.19.154.83", True),
    ("http://192.14.253.56/hello.html", True),
    ("http://localhost:443/hello.html", True),
    ("http://localhost", True),
    ("http://[2601:19b:700:b70:1106:49ab:ac46:2e12]", True),
    ("http://[2001:4860:0:2001::68]/", True),
    ("http://[::1]", True),
]


class TestIsSpecialHost(object):
    def test_basics(self):
        for hostname, result in TESTS_IS:
            assert is_special_host(hostname) == result


class TestHasSpecialHost(object):
    def test_basics(self):
        for url, result in TESTS_HAS:
            assert has_special_host(url) == result
