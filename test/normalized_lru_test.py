# -*- coding: utf-8 -*-
# =============================================================================
# Ural Normalized LRU from URL Unit Tests
# =============================================================================
from ural.lru import normalized_lru_stems

DEFAULT_TESTS = [
    ('http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2', ['t:8000', 'h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:query=mobile']),
    ('http://www.example.com/wpstyle/?p=364&q=365', ['h:com', 'h:example', 'p:wpstyle', 'p:', 'q:p=364&q=365']),
    ('www.foo.bar/index.html', ['h:bar', 'h:foo'])
]


class TestNormalizedLru(object):
    def test_basics(self):
        for url, lru in DEFAULT_TESTS:
            assert normalized_lru_stems(url) == lru

        assert normalized_lru_stems('www.foo.bar/index.html', strip_index=False) == ['h:bar', 'h:foo', 'p:index.html']
        assert normalized_lru_stems('http://www.foo.bar/index.html', strip_protocol=False) == ['s:http', 'h:bar', 'h:foo']
        assert normalized_lru_stems('www.lepopulaire.fr/', strip_trailing_slash=True) == ['h:fr', 'h:lepopulaire']
