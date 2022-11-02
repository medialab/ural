# =============================================================================
# Ural Classes Unit Tests
# =============================================================================
import pytest
from ural.classes import TrieDict


class TestTrieDict(object):
    def test_basics(self):
        trie = TrieDict()

        trie[['a', 'b', 'c']] = 123

        assert trie.get(['a', 'b', 'c']) == 123
        assert trie.get(['a', 'b']) is None
        assert trie.get([]) is None
        assert trie.get(['b', 'd']) is None
        assert trie.get(['a', 'b', 'c', 'd']) is None
        assert trie.get(['a', 'b'], 456) == 456

        trie[['a', 'b', 'c']] = 456

        assert trie.get(['a', 'b', 'c']) == 456

        assert trie[['a', 'b', 'c']] == 456

        with pytest.raises(KeyError):
            _ = trie[['a', 'b']]

    def test_none_value(self):
        trie = TrieDict()

        trie[['A', 'B']] = None

        assert len(trie) == 1
        assert trie[['A', 'B']] is None
        assert trie.get(['A', 'B']) is None
        assert list(trie.items()) == [(['A', 'B'], None)]
        assert list(trie.values()) == [None]

    def test_longest_matching_prefix_value(self):
        trie = TrieDict()

        trie['roman'] = 1
        trie['romanesque'] = 2
        trie['john'] = 3
        trie['j'] = 2

        assert len(trie) == 4

        assert trie.longest_matching_prefix_value('jo') == 2
        assert trie.longest_matching_prefix_value('a') is None
        assert trie.longest_matching_prefix_value('abcde') is None
        assert trie.longest_matching_prefix_value('johnsie') == 3
        assert trie.longest_matching_prefix_value('romani') == 1
        assert trie.longest_matching_prefix_value('romanesque') == 2
        assert trie.longest_matching_prefix_value('romanesques') == 2

    def test_iteration(self):
        trie = TrieDict()

        trie['abc'] = 1
        trie['def'] = 2

        assert set((''.join(p), v) for p, v in trie.items()) == {('abc', 1), ('def', 2)}
        assert set((''.join(p), v) for p, v in trie) == {('abc', 1), ('def', 2)}

        assert set(''.join(p) for p in trie.prefixes()) == {'abc', 'def'}
        assert set(trie.values()) == {1, 2}
