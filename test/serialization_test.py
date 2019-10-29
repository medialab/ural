# -*- coding: utf-8 -*-
# =============================================================================
# Ural Serialization LRU Unit Tests
# =============================================================================
from ural.lru import serialize_lru
from ural.lru import unserialize_lru


SERIALIZE_TESTS = [
    (['t:8000', 'h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:query=mobile'], 't:8000|h:fr|h:lemonde|p:article|p:1234|q:query=mobile|'),
    (['h:com', 'h:example', 'p:wpstyle', 'p:', 'q:p=364&q=365'], 'h:com|h:example|p:wpstyle|p:|q:p=364&q=365|'),
    (['h:bar', 'h:foo'], 'h:bar|h:foo|')
]

UNSERIALIZE_TESTS = [
    ('t:8000|h:fr|h:lemonde|p:article|p:1234|q:query=mobile|', ['t:8000', 'h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:query=mobile']),
    ('h:com|h:example|p:wpstyle|p:|q:p=364&q=365|', ['h:com', 'h:example', 'p:wpstyle', 'p:', 'q:p=364&q=365']),
    ('h:bar|h:foo|', ['h:bar', 'h:foo'])
]


class TestSerializationLru(object):
    def test_basics(self):
        for lru, lruSerialized in SERIALIZE_TESTS:
            assert serialize_lru(lru) == lruSerialized
        for lruSerialized, lru in UNSERIALIZE_TESTS:
            assert unserialize_lru(lruSerialized) == lru
