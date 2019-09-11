# =============================================================================
# Ural Facebook Unit Tests
# =============================================================================
import pytest
from ural.facebook import convert_facebook_url_to_mobile

MOBILE_TESTS = [
    ('http://www.facebook.com', 'http://m.facebook.com'),
    ('http://facebook.com', 'http://m.facebook.com'),
    ('http://fr.facebook.com', 'http://m.facebook.com'),
    ('http://fr-FR.facebook.com', 'http://m.facebook.com'),
    ('http://www.facebook.com/whatever#ok', 'http://m.facebook.com/whatever#ok'),
    ('https://www.facebook.co.uk', 'https://m.facebook.co.uk'),
    ('facebook.com', 'm.facebook.com')
]


class TestFacebook(object):
    def test_convert_facebook_url_to_mobile(self):
        for url, expected in MOBILE_TESTS:
            assert convert_facebook_url_to_mobile(url) == expected

        with pytest.raises(Exception):
            convert_facebook_url_to_mobile('http://twitter.com')
