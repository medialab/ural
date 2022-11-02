#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Has Special Host Unit Tests
# =============================================================================
from ural import has_special_host

TESTS = [
    ('http://127.0.0.1', True),
    ('http://youtube.com', False),
    ('http://104.19.154.83', True),
    ('http://192.14.253.56/hello.html', True),
    ('http://localhost:443/hello.html', True),
    ('http://localhost', True),
    ('http://[2601:19b:700:b70:1106:49ab:ac46:2e12]', True),
    ('http://[2001:4860:0:2001::68]/', True),
    ('http://[::1]', True)
]


class TestHasSpecialHost(object):
    def test_basics(self):
        for url, result in TESTS:
            assert has_special_host(url) == result
