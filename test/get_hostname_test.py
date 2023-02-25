#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Name Getter Unit Tests
# =============================================================================
from ural.get_hostname import get_hostname, get_hostname_prefixes

SUBDOMAIN_TESTS = [
    ("http://www.facebook.com", "www.facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
]


class TestGetHostname(object):
    def test_get_hostname(self):
        for url, hostname in SUBDOMAIN_TESTS:
            assert get_hostname(url) == hostname

    def test_get_hostname_prefixes(self):
        assert get_hostname_prefixes("www.lemonde.fr") == [
            "www.lemonde.fr",
            "lemonde.fr",
            "fr",
        ]

        assert get_hostname_prefixes("192.167.45.2") == ["192.167.45.2"]
