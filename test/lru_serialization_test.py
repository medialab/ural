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


class TestLruSerialization(object):
    def test_serialize(self):
        for lru, serialized in SERIALIZE_TESTS:
            assert serialize_lru(lru) == serialized

    def test_unserialized(self):
        for lru, serialized in SERIALIZE_TESTS:
            assert unserialize_lru(serialized) == lru

    def test_idempotency(self):
        for lru, serialized in SERIALIZE_TESTS:
            assert unserialize_lru(serialize_lru(lru)) == lru
            assert serialize_lru(unserialize_lru(serialized)) == serialized
