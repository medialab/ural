# =============================================================================
# Ural Twitter Unit Tests
# =============================================================================
import pytest
from ural.twitter import is_twitter_url, extract_screen_name_from_twitter_url


IS_TESTS = [
    ('https://twitter.com', True),
    ('twitter.com', True),
    ('http://www.lemonde.fr', False),
    ('http://www.twitter.com', True)
]

EXTRACT_SCREEN_NAME_TESTS = [
    ('https://twitter.com', None),
    ('https://www.lemonde.fr', None),
    ('https://twitter.com/Yomguithereal', 'yomguithereal'),
    ('https://twitter.com/yomguithereal', 'yomguithereal'),
    ('https://twitter.com/@Yomguithereal', 'yomguithereal'),
    ('https://twitter.com/Yomguithereal/', 'yomguithereal'),
    ('https://twitter.com/Yomguithereal?s=19', 'yomguithereal'),
    ('https://twitter.com/Yomguithereal#anchor', 'yomguithereal'),
    ('https://twitter.com/#!/Yomguithereal', 'yomguithereal'),
    ('http://twitter.com/Yomguithereal', 'yomguithereal'),
    ('https://twitter.com/Yomguithereal/lists', 'yomguithereal'),
    ('https://twitter.com/medialab_ScPo/status/1284154793376784385', 'medialab_scpo'),
    ('https://twitter.com/hashtag/Covid?src=hashtag_click', None),
    ('https://twitter.com/search?q=ue&src=typed_query', None),
    ('https://twitter.com/home', None),
    ('https://twitter.com/explore', None),
    ('https://twitter.com/settings', None),
    ('https://twitter.com/messages', None),
    ('https://twitter.com/notifications', None),
    ('https://twitter.com/i/notifications', None),
    ('https://twitter.com/i/timeline', None),
    ('https://twitter.com/i/bookmarks', None),
    ('twitter.com/Yomguithereal', 'yomguithereal')
]


class TestTwitter(object):
    def test_is_twitter_url(self):
        for url, result in IS_TESTS:
            assert is_twitter_url(url) == result

    def test_extract_screen_name_from_twitter_url(self):
        for url, screen_name in EXTRACT_SCREEN_NAME_TESTS:
            assert extract_screen_name_from_twitter_url(url) == screen_name
