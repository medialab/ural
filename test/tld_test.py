#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Hostname Name Getter Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural.tld import (
    get_domain_name,
    is_valid_tld,
    has_valid_tld,
    split_suffix,
    has_valid_suffix,
)

GET_DOMAIN_NAME_TESTS = [
    ("http://facebook.com/whatever", "facebook.com"),
    ("facebook.com/whatever", "facebook.com"),
    ("notatld.blablablou", None),
    ("HTTP://GOOGLE.COM", "google.com"),
    ("", None),
]

IS_VALID_TLD_TESTS = [
    ("com", True),
    (".com", True),
    (".megalol", False),
    (".xn--fiqs8s", True),
    ("中国", True),
    ("", False),
]

HAS_VALID_TLD_TESTS = [
    ("http://facebook.com/whatever", True),
    ("lemonde.showtime", True),
    ("https://test.idontexistlol", False),
    ("", False),
]

HAS_VALID_SUFFIX_TESTS = [
    ("http://www.google.co.uk", True),
    ("lemonde.showtime", True),
    ("notatld.blablablou", False),
    ("", False),
]

SPLIT_SUFFIX_TESTS = [
    ("http://facebook.com/whatever", ("facebook", "com")),
    ("business.lemonde.co.uk", ("business.lemonde", "co.uk")),
    ("notatld.blablablou", None),
    ("https://2001:0db8:0000:85a3:0000:0000:ac1f:8001", None),
    ("http://192.169.1.1", None),
    ("http://localhost:8080", None),
    ("http://localhost", None),
    ("", None),
    ("http://google.co.uk", ("google", "co.uk")),
    ("http://www.v2.google.co.uk", ("www.v2.google", "co.uk")),
    ("http://хром.гугл.рф", ("хром.гугл", "рф")),
    ("http://www.google.co.uk:8001/lorem-ipsum/", ("www.google", "co.uk")),
    ("http://www.me.cloudfront.net", ("www.me", "cloudfront.net")),
    ("https://pantheon.io/", ("pantheon", "io")),
    ("http://foo@bar.com", ("bar", "com")),
    ("http://user:foo@bar.com", ("bar", "com")),
    ("https://faguoren.xn--fiqs8s", ("faguoren", "xn--fiqs8s")),
    ("faguoren.中国", ("faguoren", "中国")),
    ("blogs.lemonde.paris", ("blogs.lemonde", "paris")),
    ("axel.brighton.ac.uk", ("axel.brighton", "ac.uk")),
    ("m.fr.blogspot.com.au", ("m.fr", "blogspot.com.au")),
    ("help.www.福岡.jp", ("help.www", "福岡.jp")),
    ("syria.arabic.variant.سوريا", ("syria.arabic.variant", "سوريا")),
    ("http://www.help.kawasaki.jp", ("www", "help.kawasaki.jp")),
    ("http://help.kawasaki.jp", ("", "help.kawasaki.jp")),
    ("http://fedoraproject.org", ("fedoraproject", "org")),
    ("http://www.cloud.fedoraproject.org", ("www", "cloud.fedoraproject.org")),
    (
        "https://www.john.app.os.fedoraproject.org",
        ("www.john", "app.os.fedoraproject.org"),
    ),
    ("ftp://www.xn--mxail5aa.xn--11b4c3d", ("www.xn--mxail5aa", "xn--11b4c3d")),
    ("http://cloud.fedoraproject.org/article.html", ("", "cloud.fedoraproject.org")),
    ("github.io", ("", "github.io")),
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

    def test_has_valid_suffix(self):
        for url, result in HAS_VALID_SUFFIX_TESTS:
            assert has_valid_suffix(url) == result

        for url, result in SPLIT_SUFFIX_TESTS:
            assert has_valid_suffix(url) == (result is not None)

    def test_split_suffix(self):
        for url, result in SPLIT_SUFFIX_TESTS:
            assert split_suffix(url) == result
