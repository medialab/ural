#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Name Getter Unit Tests
# =============================================================================
from ural.tld import get_domain_name, is_valid_tld, has_valid_tld

GET_DOMAIN_NAME_TESTS = [
    ("http://facebook.com/whatever", "facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
    ("notatld.blablablou", None),
]

IS_VALID_TLD_TESTS = [("com", True), (".com", True), (".megalol", False)]

HAS_VALID_TLD_TESTS = [
    ("http://facebook.com/whatever", True),
    ("lemonde.showtime", True),
    ("https://test.idontexistlol", False),
]


class TestGetDomainName(object):
    def test_get_domain_name(self):
        for url, domain in GET_DOMAIN_NAME_TESTS:
            assert get_domain_name(url) == domain

    def test_is_valid_tld(self):
        for tld, result in IS_VALID_TLD_TESTS:
            assert is_valid_tld(tld) == result

    def test_has_valid_tld(self):
        for url, result in HAS_VALID_TLD_TESTS:
            assert has_valid_tld(url) == result
