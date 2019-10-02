#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Is URL Unit Tests
# =============================================================================
from ural import is_url

DEFAULT_TESTS = [
    ('https://www.example.com/foo/?bar=baz&inga=42&quux', True),
    ('http://www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/', False),
    ('lemonde.fr/index.html', False),
    ('http://foo.com/blah_(wikipedia)#cite-1', True),
    ('http://223.255.255.254', True),
    ('http://??', False),
    ('http://../', False),
    ('http://-error-.invalid/', False),
    ('http://lemonde.fr///a/./b/..', True),
    (u'http://例子.测试', True),
    (u'http://مثال.إختبار', True),
    ('http://a.b-.co', False),
    ('http://.www.foo.bar/', False),
    ('http://www.foo.bar./', True),
    ('', False),
    ('    ', False)
]

NO_PROTOCOL_TESTS = [
    ('https://www.example.com/foo/?bar=baz&inga=42&quux', True),
    ('www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/', False),
    ('lemonde.fr/index.html', True),
    ('foo.com/blah_(wikipedia)#cite-1', True),
    ('223.255.255.254', True),
    ('??', False),
    ('../', False),
    ('-error-.invalid/', False),
    ('lemonde.fr///a/./b/..', True),
    (u'例子.测试', True),
    (u'مثال.إختبار', True),
    ('a.b-.co', False),
    ('.www.foo.bar/', False),
    ('www.foo.bar./', True),
    ('lemonde.fr/economie/article.php', True),
    ('', False),
    ('    ', False)
]

TLD_AWARE_TESTS = [
    ('http://lemonde.fr', True),
    ('http://www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/', False),
    ('https://lemonde.co.uk', True),
    ('http://lemonde.mesfesses', False),
    ('lemonde.watashiwa', False),
    ('lefigaro.fr', True),
    ('', False),
    ('    ', False)
]


class TestIsUrl(object):
    def test_basics(self):

        for url, result in DEFAULT_TESTS:
            assert is_url(url) == result

        for url, result in NO_PROTOCOL_TESTS:
            assert is_url(url, require_protocol=False) == result

        for url, result in TLD_AWARE_TESTS:
            assert is_url(url, require_protocol=False, tld_aware=True) == result
