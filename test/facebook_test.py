# =============================================================================
# Ural Facebook Unit Tests
# =============================================================================
import pytest
from ural.facebook import (
    is_facebook_url,
    convert_facebook_url_to_mobile,
    extract_user_from_facebook_url
)

MOBILE_TESTS = [
    ('http://www.facebook.com', 'http://m.facebook.com'),
    ('http://facebook.com', 'http://m.facebook.com'),
    ('http://fr.facebook.com', 'http://m.facebook.com'),
    ('http://fr-FR.facebook.com', 'http://m.facebook.com'),
    ('http://www.facebook.com/whatever#ok', 'http://m.facebook.com/whatever#ok'),
    ('https://www.facebook.co.uk', 'https://m.facebook.co.uk'),
    ('facebook.com', 'm.facebook.com')
]

USER_EXTRACT_TESTS = [
    ('/naat.ouhafs.92?rc=p&__tn__=R', 'naat.ouhafs.92', 'handle'),
    ('naat.ouhafs.92?rc=p&__tn__=R', 'naat.ouhafs.92', 'handle'),
    ('http://fr-fr.facebook.com/naat.ouhafs.92?rc=p&__tn__=R', 'naat.ouhafs.92', 'handle'),
    ('fr-fr.facebook.com/naat.ouhafs.92?rc=p&__tn__=R', 'naat.ouhafs.92', 'handle'),
    ('facebook.com/naat.ouhafs.92?rc=p&__tn__=R', 'naat.ouhafs.92', 'handle'),
    ('/profile.php?id=100012241140363&rc=p&__tn__=R', '100012241140363', 'id'),
    ('profile.php?id=100012241140363&rc=p&__tn__=R', '100012241140363', 'id'),
    ('https://www.facebook.com/profile.php?id=100012241140363&rc=p&__tn__=R', '100012241140363', 'id'),
    ('https://facebook.com/profile.php?id=100012241140363&rc=p&__tn__=R', '100012241140363', 'id'),
    ('facebook.com/profile.php?id=100012241140363&rc=p&__tn__=R', '100012241140363', 'id'),
    ('https://www.facebook.com/people/Clare-Roche/100020635422861', '100020635422861', 'id')
]

IS_FACEBOOK_URL_TESTS = [
    ('http://www.facebook.com/profile.php?id=398633', True),
    ('facebook.com', True),
    ('http://lemonde.fr', False),
    ('fr-FR.facebook.fr', True),
    ('http://m.facebook.com', True),
    ('https://fb.me/47574', True)
]


class TestFacebook(object):
    def test_convert_facebook_url_to_mobile(self):
        for url, expected in MOBILE_TESTS:
            assert convert_facebook_url_to_mobile(url) == expected

        with pytest.raises(Exception):
            convert_facebook_url_to_mobile('http://twitter.com')

    def test_extract_user_from_facebook_url(self):
        for url, target, kind in USER_EXTRACT_TESTS:
            user = extract_user_from_facebook_url(url)
            comparison = user.id if kind == 'id' else user.handle

            assert comparison == target

    def test_is_facebook_url(self):
        for url, result in IS_FACEBOOK_URL_TESTS:
            assert is_facebook_url(url) == result
