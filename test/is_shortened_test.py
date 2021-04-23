#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Shortened URL Unit Tests
# =============================================================================
from ural import is_shortened_url

TESTS = [
    ('http://lemonde.fr', False),
    ('lemonde.fr', False),
    ('https://t.co/yusF6sIMv7?amp=1', True),
    ('t.co/yusF6sIMv7?amp=1', True),
    ('http://bit.ly/1sNZMwL', True),
    ('http://localhost:8000', False),
    ('https://192.168.0.1', False)
]


class TestIsShortenedUrl(object):
    def test_basics(self):
        for url, result in TESTS:
            assert is_shortened_url(url) == result
