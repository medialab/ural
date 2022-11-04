#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is URL Unit Tests
# =============================================================================
from ural import is_url

DEFAULT_TESTS = [
    ("https://www.example.com/foo/?bar=baz&inga=42&quux", True),
    (
        "http://www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/",
        False,
    ),
    ("lemonde.fr/index.html", False),
    ("http://foo.com/blah_(wikipedia)#cite-1", True),
    ("http://223.255.255.254", True),
    ("http://??", False),
    ("http://../", False),
    ("http://-error-.invalid/", False),
    ("http://lemonde.fr///a/./b/..", True),
    ("http://例子.测试", True),
    ("http://مثال.إختبار", True),
    ("http://a.b-.co", False),
    ("http://.www.foo.bar/", False),
    ("http://www.foo.bar./", True),
    ("http://lemonde.fr/path with spaces", False),
    ("http://localhost", True),
    ("https://localhost:80/test.html", True),
    ("http://xn--bcher-kva.ch/index.html", True),
    ("http://bücher.ch/index.html", True),
    ("", False),
    ("    ", False),
]

NO_PROTOCOL_TESTS = [
    ("https://www.example.com/foo/?bar=baz&inga=42&quux", True),
    (
        "www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/",
        False,
    ),
    ("lemonde.fr/index.html", True),
    ("foo.com/blah_(wikipedia)#cite-1", True),
    ("223.255.255.254", True),
    ("??", False),
    ("../", False),
    ("-error-.invalid/", False),
    ("lemonde.fr///a/./b/..", True),
    ("例子.测试", True),
    ("مثال.إختبار", True),
    ("a.b-.co", False),
    (".www.foo.bar/", False),
    ("www.foo.bar./", True),
    ("lemonde.fr/economie/article.php", True),
    ("localhost", True),
    ("", False),
    ("    ", False),
]

TLD_AWARE_TESTS = [
    ("http://lemonde.fr", True),
    (
        "http://www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/",
        False,
    ),
    ("https://lemonde.co.uk", True),
    ("http://lemonde.mesfesses", False),
    ("lemonde.watashiwa", False),
    ("http://user@lemonde.fr", True),
    ("http://user:mdp@lemonde.fr:7474", True),
    ("http://user:mdp@lemonde.mesfesses", False),
    ("lefigaro.fr", True),
    ("http://localhost", True),
    ("localhost", True),
    ("https://192.168.1.1", True),
    ("http://127.0.0.1", True),
    ("127.0.0.1", True),
    ("http://194.245.235.98/test", True),
    ("http://user:mdp@194.245.235.98/test", True),
    (
        "http://91.212.7.144/hronika/tanjug-makron-zbog-politicke-krize-u-francuskoj-da-pomeri-posetu-srbiji.html",
        True,
    ),
    ("", False),
    ("    ", False),
]

RELAXED_TESTS = [
    ("http://lemonde.fr", True),
    ("http://lemonde.fr/path/is/ok", True),
    ("http://lemonde.fr/path with spaces", True),
    ("lemonde.fr/path with spaces", True),
    (
        "http://www.jura.gouv.fr/content/download/17618/129500/file/agenda public pr%C3%A9visionnel du pr%C3%A9fet du Jura- semaine 31.pdf",
        True,
    ),
]

ONLY_HTTP_HTTPS_TESTS = [
    ("http://lemonde.fr", True),
    ("wss://lemonde.fr/websockets", False),
]


class TestIsUrl(object):
    def test_basics(self):

        for url, result in DEFAULT_TESTS:
            assert is_url(url) == result

        for url, result in NO_PROTOCOL_TESTS:
            assert is_url(url, require_protocol=False) == result

        for url, result in TLD_AWARE_TESTS:
            assert is_url(url, require_protocol=False, tld_aware=True) == result

        for url, result in RELAXED_TESTS:
            assert (
                is_url(url, require_protocol=False, allow_spaces_in_path=True) == result
            )

        for url, result in ONLY_HTTP_HTTPS_TESTS:
            assert is_url(url, only_http_https=True) == result
