# =============================================================================
# Ural Facebook Unit Tests
# =============================================================================
import pytest
from ural.facebook import (
    is_facebook_url,
    convert_facebook_url_to_mobile,
    extract_user_from_facebook_url,
    is_facebook_link,
    extract_url_from_facebook_link
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

FACEBOOK_LINK_TESTS = [
    (
        'https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.chaos-controle.com%2Farchives%2F2013%2F10%2F14%2F28176300.html&amp;h=AT0iUqJpUTMzHAH8HAXwZ11p8P3Z-SrY90wIXZhcjMnxBTHMiau8Fv1hvz00ZezRegqmF86SczyUXx3Gzdt_MdFH-I4CwHIXKKU9L6w522xwOqkOvLAylxojGEwrp341uC-GlVyGE2N7XwTPK9cpP0mQ8PIrWh8Qj2gHIIR08Js0mUr7G8Qe9fx66uYcfnNfTTF1xi0Us8gTo4fOZxAgidGWXsdgtU_OdvQqyEm97oHzKbWfXjkhsrzbtb8ZNMDwCP5099IMcKRD8Hi5H7W3vwh9hd_JlRgm5Z074epD_mGAeoEATE_QUVNTxO0SHO4XNn2Z7LgBamvevu1ENBcuyuSOYA0BsY2cx8mPWJ9t44tQcnmyQhBlYm_YmszDaQx9IfVP26PRqhsTLz-kZzv0DGMiJFU78LVWVPc9QSw2f9mA5JYWr29w12xJJ5XGQ6DhJxDMWRnLdG8Tnd7gZKCaRdqDER1jkO72u75-o4YuV3CLh4j-_4u0fnHSzHdVD8mxr9pNEgu8rvJF1E2H3-XbzA6F2wMQtFCejH8MBakzYtTGNvHSexSiKphE04Ci1Z23nBjCZFsgNXwL3wbIXWfHjh2LCKyihQauYsnvxp6fyioStJSGgyA9GGEswizHa20lucQF0S0F8H9-',
        'http://www.chaos-controle.com/archives/2013/10/14/28176300.html'
    ),
    (
        'https://www.lemonde.fr',
        None
    ),
    (
        'https://lm.facebook.com/l.php?u=https%3A%2F%2Fwww.santeplusmag.com%2Fvoici-homme-ideal-selon-signe-zodiaque%2F%3Ffbclid%3DIwAR0y7QtbwjHkA5xGt-JpiINpi5sx9bBdqPgVZlLoY4QXGr7eyHum1wA1tgw&h=AT0JS8tV0L4V23RGMkKsnQNfkt2k9ncZ39JltGuSXqro1LpLQw-kUxgTo2QJprUxH9WS3HpZvb5XRsv3pKJyo6yRF5Zpw6qZRorVGSwiKlD8L5LOmUstIPrGrdboG-OMBDzrGQOU5yONWyjEGlNIZDEpcGSzz4ZZi8IRq6FU-fX385WrAbToCn8AahZXz1_fPFz7bzaDEiHhgM0PHd4iHtF5T-h0lqLlVoqVOMAKU9X2Of2Ief9xWBqlaszvlo816PgMDDhYBkM1TUfevQDa1seXKHdYHKLaHz1LQEIlUlbZnINwWHq9qdgO0KR6Zml2jSsts8ttdxwn8-YYmiRuGy14DWb_-h8WU-_j4O6dWo-9oEfXP_V4RS9ZCkB1aTiaTy1-d92EtVaii24vDuxF_k7VzjZmlA3IToH0weg269bRO_4adejJuYRlaCQFsEhtwom9BqWriXYfdYznFd0po5vHTE9h7ZDRN7jvYSiACSShPnD_xfDiIsQOkE11J4qft7J5ZsHhYk0i2e3WwOqUsK_-kb7aEdeLO3Na7tOfO1UkxlAkCcpANn3ZBBFfjTu4yBQDmuQ7eBMQHUmvRDp96p2EuYPGjsCYP_sXH5dwZ6wKB5GzunmtexIMwiVaIHdOeM42e435pSk0nD3XZhU15qday5GelcMfwHsbN8kzAdvJSRK5EmbVX0dPWsIk5GEVEhqNOOT0ANFz85bXB8nSbLkNk1NLkWd6cwGHVOmmW6Vgl15FzUJKwfoya-owBE9aQhItB_MANmkajA98vAuuAwe1Wfw1MGDuOKUzBNp6ercFpO1diFR-N9SvTxfKc-ZCu0lQKXOcgT3qpe5usMmxcXg6TUCC7ox0pu_j8ees4fF-JQIddh5DDQm5sXOajqKKDEj1-hDL15oW_z_NRuRkXAxhLXN1s5vWt_cDuxHuqwlKI3wst9fK31Z1ovRk0HJa_deZ47E81QxPGlcWFUp3If2tPqE5qiiX6yfRD3QriMMH04wDnSN-R8gYjQKydKQpF_B9tn1BfEvIiOK21kgtzvgnu6iJRTfrNS9qRD1HJcMkf_W5fWPPk1HMc6VtEgf-uU7xxZ1heqj52nVUoMJl3pWV2dlv44KOIPM9afoRddeRH3RDl7B8nbabEER0zsVjGgkre6qLRgKz5P2M8BJJJtCo',
        'https://www.santeplusmag.com/voici-homme-ideal-selon-signe-zodiaque/?fbclid=IwAR0y7QtbwjHkA5xGt-JpiINpi5sx9bBdqPgVZlLoY4QXGr7eyHum1wA1tgw'
    )
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

    def test_extract_url_from_facebook_link(self):
        for link, url in FACEBOOK_LINK_TESTS:
            assert extract_url_from_facebook_link(link) == url

    def test_is_facebook_link(self):
        for link, url in FACEBOOK_LINK_TESTS:
            assert is_facebook_link(link) == (url is not None)
