#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Special Host Unit Tests
# =============================================================================
from ural import is_special_host

TESTS = [
    ('127.0.0.1', True),
    ('youtube.com', False),
    ('104.19.154.83', True),
    ('192.14.253.56', True),
    ('localhost:443', True),
    ('localhost', True),
    ('2601:19b:700:b70:1106:49ab:ac46:2e12', True),
    ('2001:4860:0:2001::68', True),
    ('::1', True)
]


class TestIsSpecialHost(object):
    def test_basics(self):
        for hostname, result in TESTS:
            assert is_special_host(hostname) == result
