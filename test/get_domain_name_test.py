#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Domain Name Getter Unit Tests
# =============================================================================
from ural import get_domain_name, get_hostname

DOMAIN_TESTS = [
    ('http://facebook.com/whatever', 'facebook.com'),
    ('facebook.com/whatever', 'facebook.com'),
    ('notatld.blablablou', None)
]

SUBDOMAIN_TESTS = [
    ('http://www.facebook.com', 'www.facebook.com'),
    ('facebook.com/whatever', 'facebook.com')
]


class TestGetDomainName(object):
    def test_get_domain_name(self):
        for url, domain in DOMAIN_TESTS:
            assert get_domain_name(url) == domain

    def test_get_hostname(self):
        for url, hostname in SUBDOMAIN_TESTS:
            assert get_hostname(url) == hostname
