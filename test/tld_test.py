#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Name Getter Unit Tests
# =============================================================================
from ural import get_domain_name

DOMAIN_TESTS = [
    ("http://facebook.com/whatever", "facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
    ("notatld.blablablou", None),
]


class TestGetDomainName(object):
    def test_get_domain_name(self):
        for url, domain in DOMAIN_TESTS:
            assert get_domain_name(url) == domain
