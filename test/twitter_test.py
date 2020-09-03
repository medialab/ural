# =============================================================================
# Ural Twitter Unit Tests
# =============================================================================
import pytest
from ural.twitter import (
    is_twitter_url
)

IS_TESTS = [
    ('https://twitter.com', True),
    ('twitter.com', True),
    ('http://www.lemonde.fr', False),
    ('http://www.twitter.com', True),
    ('http://twitter.fr/whatever', True)
]


class TestTwitter(object):
    def test_is_twitter_url(self):
        for url, result in IS_TESTS:
            assert is_twitter_url(url) == result
