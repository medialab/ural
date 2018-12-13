#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Is URL Unit Tests
# =============================================================================
from ural import is_url

DEFAULT_TESTS = [
    ('https://www.example.com/foo/?bar=baz&inga=42&quux', True),
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
    ('http://www.foo.bar./', False)
]

NO_PROTOCOL_TESTS = [
    ('https://www.example.com/foo/?bar=baz&inga=42&quux', True),
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
    ('www.foo.bar./', False)
]


class TestStripProtocol(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert is_url(url) == result
        for url, result in NO_PROTOCOL_TESTS:
            assert is_url(url, require_protocol=False) == result
