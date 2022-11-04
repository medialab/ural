# =============================================================================
# Ural Telegram Unit Tests
# =============================================================================
from ural.telegram import (
    is_telegram_url,
    parse_telegram_url,
    is_telegram_message_id,
    convert_telegram_url_to_public,
    extract_channel_name_from_telegram_url,
    TelegramGroup,
    TelegramMessage,
    TelegramChannel,
)

IS_TESTS = [
    ("https://youtube.com", False),
    ("http://www.lemonde.fr", False),
    ("https://t.me/s/katroulo/76", True),
    ("https://telegram.me/guigougu", True),
    ("https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w", True),
    ("http://telegram.org", True),
]

MOBILE_TESTS = [
    ("http://www.telegram.org", "http://t.me/s"),
    ("http://telegram.me/whatever#ok", "http://t.me/s/whatever#ok"),
    ("telegram.me", "t.me/s"),
    ("https://t.me/katroulo/76", "https://t.me/s/katroulo/76"),
    ("https://telegram.me/guigougu", "https://t.me/s/guigougu"),
]

PARSE_TESTS = [
    ("https://youtube.com", None, "https://youtube.com"),
    ("http://www.lemonde.fr", None, "http://www.lemonde.fr"),
    (
        "https://t.me/s/katroulo/76",
        TelegramMessage(name="katroulo", id="76"),
        "https://t.me/s/katroulo/76",
    ),
    (
        "https://telegram.me/guigougu",
        TelegramChannel(name="guigougu"),
        "https://telegram.me/guigougu",
    ),
    (
        "https://telegram.me/s/joinchat/AAAAAE9B8u_wO9d4NiJp3w",
        TelegramGroup(id="AAAAAE9B8u_wO9d4NiJp3w"),
        "https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w",
    ),
    (
        "https://telegram.me/katroulo/76",
        TelegramMessage(name="katroulo", id="76"),
        "https://t.me/s/katroulo/76",
    ),
    (
        "https://t.me/s/guigougu",
        TelegramChannel(name="guigougu"),
        "https://telegram.me/guigougu",
    ),
    (
        "https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w",
        TelegramGroup(id="AAAAAE9B8u_wO9d4NiJp3w"),
        "https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w",
    ),
    (
        "https://t.me/joinchat/s/AAAAAE9B8u_wO9d4NiJp3w",
        TelegramGroup(id="AAAAAE9B8u_wO9d4NiJp3w"),
        "https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w",
    ),
]


class TestTelegram(object):
    def test_convert_telegram_url_to_public(self):
        for url, expected in MOBILE_TESTS:
            assert convert_telegram_url_to_public(url) == expected

    def test_is_telegram_id(self):
        assert not is_telegram_message_id("test")
        assert is_telegram_message_id("8745346")

    def test_is_telegram_url(self):
        for url, result in IS_TESTS:
            assert is_telegram_url(url) == result

    def test_parse_telegram_url(self):
        for url, result, _ in PARSE_TESTS:
            assert parse_telegram_url(url) == result

    def test_extract_channel_name_from_telegram_url(self):
        for url, result, _ in PARSE_TESTS:
            extract_result = (
                None
                if result is None or isinstance(result, TelegramGroup)
                else result.name
            )

            assert extract_channel_name_from_telegram_url(url) == extract_result
