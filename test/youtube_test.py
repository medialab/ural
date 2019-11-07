# =============================================================================
# Ural Youtube Unit Tests
# =============================================================================
import pytest
from ural.youtube import (
    is_youtube_url
)

IS_YOUTUBE_URL_TESTS = [
    ('https://youtube.com', True),
    ('youtu.be/ugèètef', True),
    ('http://www.lemonde.fr', False)
]


class TestYoutube(object):
    def test_is_youtube_url(self):
        for url, result in IS_YOUTUBE_URL_TESTS:
            assert is_youtube_url(url) == result
