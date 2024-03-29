# coding: utf-8
# =============================================================================
# Ural Instagram Unit Tests
# =============================================================================
from ural.instagram import (
    is_instagram_url,
    parse_instagram_url,
    is_instagram_post_shortcode,
    is_instagram_username,
    extract_username_from_instagram_url,
    InstagramPost,
    InstagramUser,
    InstagramReel,
)

IS_TESTS = [
    ("https://youtube.com", False),
    ("http://www.lemonde.fr", False),
    ("https://www.instagram.com/p/BxKRx5CHn5i/", True),
    (
        "https://www.instagram.com/p/BxKRx5CHn5i/?utm_source=ig_share_sheet&igshid=znsinsart176",
        True,
    ),
    ("https://www.instagram.com/p/BxKRx5-Hn5i/", True),
    ("https://www.instagram.com/martin/p/BxKRx5C_n5i/", True),
    ("https://www.instagram.com/martin_dupont/p/BxKRx5CHn5i/", True),
    ("https://www.instagram.com/martin", True),
    ("https://www.instagram.com/martin_dupont/", True),
    ("https://www.instagram.com/reel/Co-r5ZyTuZ--/", True),
]

PARSE_TESTS = [
    ("https://youtube.com", None, "https://youtube.com"),
    ("http://www.lemonde.fr", None, "http://www.lemonde.fr"),
    (
        "https://www.instagram.com/p/BxKRx5CHn5i/",
        InstagramPost(id="BxKRx5CHn5i", name=None),
        "https://www.instagram.com/p/BxKRx5CHn5i/",
    ),
    (
        "https://www.instagram.com/p/BxKRx5CHn5i/?utm_source=ig_share_sheet&igshid=znsinsart176",
        InstagramPost(id="BxKRx5CHn5i", name=None),
        "https://www.instagram.com/p/BxKRx5CHn5i/?utm_source=ig_share_sheet&igshid=znsinsart176",
    ),
    (
        "https://www.instagram.com/p/BxKRx5-Hn5i/",
        InstagramPost(id="BxKRx5-Hn5i", name=None),
        "https://www.instagram.com/p/BxKRx5-Hn5i/",
    ),
    (
        "https://www.instagram.com/martin/p/BxKRx5C_n5i/",
        InstagramPost(id="BxKRx5C_n5i", name="martin"),
        "https://www.instagram.com/martin/p/BxKRx5C_n5i/",
    ),
    (
        "https://www.instagram.com/martin_dupont/p/BxKRx5CHn5i/",
        InstagramPost(id="BxKRx5CHn5i", name="martin_dupont"),
        "https://www.instagram.com/martin_dupont/p/BxKRx5CHn5i/",
    ),
    (
        "https://www.instagram.com/martin",
        InstagramUser(name="martin"),
        "https://www.instagram.com/martin",
    ),
    (
        "https://www.instagram.com/martin_dupont/",
        InstagramUser(name="martin_dupont"),
        "https://www.instagram.com/martin_dupont/",
    ),
    (
        "https://www.instagram.com/reel/",
        InstagramUser(name="reel"),
        "https://www.instagram.com/reel/",
    ),
    (
        "https://www.instagram.com/reel/Co-r5ZyTuZ--/",
        InstagramReel(id="Co-r5ZyTuZ--"),
        "https://www.instagram.com/reel/Co-r5ZyTuZ--/",
    ),
    (
        "https://www.instagram.com/reels/Co2ZFRrAgHy/",
        InstagramReel(id="Co2ZFRrAgHy"),
        "https://www.instagram.com/reels/Co2ZFRrAgHy/",
    ),
    (
        "https://www.instagram.com/reels/videos/Co2ZFRrAgHy/",
        InstagramReel(id="Co2ZFRrAgHy"),
        "https://www.instagram.com/reels/videos/Co2ZFRrAgHy/",
    ),
    ("https://www.instagram.com/reels/", None, "https://www.instagram.com/reels/"),
    (
        "https://www.instagram.com/reels/videos",
        None,
        "https://www.instagram.com/reels/videos",
    ),
    (
        "https://www.instagram.com/reels/videos/videos",
        None,
        "https://www.instagram.com/reels/videos/videos",
    ),
    ("https://www.instagram.com/direct/", None, "https://www.instagram.com/direct/"),
    (
        "https://www.instagram.com/your_activity/interactions/likes/",
        None,
        "https://www.instagram.com/your_activity/interactions/likes/",
    ),
]


class TestInstagram(object):
    def test_is_instagram_post_shortcode(self):
        assert is_instagram_post_shortcode("test")
        assert is_instagram_post_shortcode("8745346")
        assert is_instagram_post_shortcode("BxKRx_C-n5i")
        assert not is_instagram_post_shortcode("BxKRx5ùHn5i")

    def test_is_instagram_username(self):
        assert is_instagram_username("test")
        assert is_instagram_username("8745346")
        assert is_instagram_username("BxKR.x_C-n5i")
        assert not is_instagram_username("BxKRxéCHn5i")

    def test_is_instagram_url(self):
        for url, result in IS_TESTS:
            assert is_instagram_url(url) == result

    def test_parse_instagram_url(self):
        for url, result, _ in PARSE_TESTS:
            assert parse_instagram_url(url) == result

    def test_extract_username_from_instagram_url(self):
        for url, result, _ in PARSE_TESTS:
            extract_result = (
                result.name
                if isinstance(result, (InstagramPost, InstagramUser))
                else None
            )

            assert extract_username_from_instagram_url(url) == extract_result
