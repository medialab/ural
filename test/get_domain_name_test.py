#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Domain Name Getter Unit Tests
# =============================================================================
from ural import get_domain_name, get_hostname
from ural.get_domain_name import get_hostname_prefixes

DOMAIN_TESTS = [
    ("http://facebook.com/whatever", "facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
    ("notatld.blablablou", None),
]

SUBDOMAIN_TESTS = [
    ("http://www.facebook.com", "www.facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
]


class TestGetDomainName(object):
    def test_get_domain_name(self):
        for url, domain in DOMAIN_TESTS:
            assert get_domain_name(url) == domain

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
