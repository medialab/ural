#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Domain Name Getter Unit Tests
# =============================================================================
from ural import get_domain_name

TESTS = [
    ('http://facebook.com/whatever', 'facebook.com'),
    ('facebook.com/whatever', 'facebook.com'),
    ('notatld.blablablou', None)
]


class TestGetDomainName(object):
    def test_basics(self):
        for url, domain in TESTS:
            assert get_domain_name(url) == domain
