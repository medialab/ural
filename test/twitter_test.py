# =============================================================================
# Ural Twitter Unit Tests
# =============================================================================
from ural.twitter import (
    is_twitter_url,
    extract_screen_name_from_twitter_url,
    parse_twitter_url,
    TwitterTweet,
    TwitterUser,
    TwitterList,
)


IS_TESTS = [
    ("https://twitter.com", True),
    ("twitter.com", True),
    ("http://www.lemonde.fr", False),
    ("http://www.twitter.com", True),
    ("https://x.com/DoesNotExist/status/1598743914602613250?s=20", True),
]

EXTRACT_SCREEN_NAME_TESTS = [
    ("https://twitter.com", None),
    ("https://www.lemonde.fr", None),
    ("https://twitter.com/Yomguithereal", "yomguithereal"),
    ("https://twitter.com/yomguithereal", "yomguithereal"),
    ("https://x.com/Yomguithereal", "yomguithereal"),
    ("https://twitter.com/@Yomguithereal", "yomguithereal"),
    ("https://twitter.com/Yomguithereal/", "yomguithereal"),
    ("https://twitter.com/Yomguithereal?s=19", "yomguithereal"),
    ("https://twitter.com/Yomguithereal#anchor", "yomguithereal"),
    ("https://twitter.com/#!/Yomguithereal", "yomguithereal"),
    ("http://twitter.com/Yomguithereal", "yomguithereal"),
    ("https://twitter.com/Yomguithereal/lists", "yomguithereal"),
    ("https://twitter.com/medialab_ScPo/status/1284154793376784385", "medialab_scpo"),
    ("https://twitter.com/hashtag/Covid?src=hashtag_click", None),
    ("https://twitter.com/search?q=ue&src=typed_query", None),
    ("https://twitter.com/home", None),
    ("https://twitter.com/explore", None),
    ("https://twitter.com/settings", None),
    ("https://twitter.com/messages", None),
    ("https://twitter.com/notifications", None),
    ("https://twitter.com/i/notifications", None),
    ("https://twitter.com/i/timeline", None),
    ("https://twitter.com/i/bookmarks", None),
    ("twitter.com/Yomguithereal", "yomguithereal"),
    ("twitter.com/Yomguithereal/#!/boogheta", "yomguithereal"),
    ("twitter.com/home/#!/boogheta", None),
    ("twitter.com/#whatever", None),
    ("twitter.com/#!boogheta", "boogheta"),
    ("twitter.com#!boogheta", "boogheta"),
    ("twitter.com/#!@boogheta", "boogheta"),
    ("twitter.com/#!/@boogheta", "boogheta"),
]

PARSE_TWEET_URL_TESTS = [
    (
        "https://twitter.com/NetflixFR/status/1455202987844857861",
        TwitterTweet(user_screen_name="netflixfr", id="1455202987844857861"),
    ),
    (
        "twitter.com/#!/@boogheta/statuses/1250082665765666816",
        TwitterTweet(user_screen_name="boogheta", id="1250082665765666816"),
    ),
    ("https://twitter.com", None),
    (
        "https://twitter.com/Yomguithereal?s=19",
        TwitterUser(screen_name="yomguithereal"),
    ),
    (
        "https://x.com/Yomguithereal?s=19",
        TwitterUser(screen_name="yomguithereal"),
    ),
    ("https://twitter.com/notifications", None),
    ("twitter.com/#whatever", None),
    ("twitter.com#!boogheta", TwitterUser(screen_name="boogheta")),
    ("https://twitter.com/home", None),
    (
        "https://twitter.com/i/lists/1551265122798157826",
        TwitterList(id="1551265122798157826"),
    ),
    ("https://twitter.com/i/lists/", None),
]


class TestTwitter(object):
    def test_is_twitter_url(self):
        for url, result in IS_TESTS:
            assert is_twitter_url(url) == result

    def test_extract_screen_name_from_twitter_url(self):
        for url, screen_name in EXTRACT_SCREEN_NAME_TESTS:
            assert extract_screen_name_from_twitter_url(url) == screen_name, url

    def test_parse_twitter_url(self):
        for url, results in PARSE_TWEET_URL_TESTS:
            assert parse_twitter_url(url) == results
