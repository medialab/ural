# =============================================================================
# Ural URL Normalization Unit Tests
# =============================================================================
from ural import normalize_url

TESTS = [
    ('http://lemonde.fr///a/./b/..', 'lemonde.fr/a'),
    ('lemonde.fr/index.html', 'lemonde.fr'),
    ('lemonde.fr/index.php', 'lemonde.fr'),
    ('lemonde.fr/index.php?utm_content=whatever&test=toto', 'lemonde.fr?test=toto'),
    ('lemonde.fr/index.php?utm_content=whatever', 'lemonde.fr'),
    ('https://lemonde.fr?', 'lemonde.fr'),
    ('https://lemonde.fr#anchor', 'lemonde.fr'),
    ('https://lemonde.fr/#anchor', 'lemonde.fr/'),
    ('https://lemonde.fr/#/path/is/here', 'lemonde.fr/#/path/is/here'),
    ('https://lemonde.fr#!/path/is/here', 'lemonde.fr#!/path/is/here'),
    ('//www.lemonde.fr', 'lemonde.fr'),
    ('//www.lemonde.fr?XTOR=whatev', 'lemonde.fr'),
    ('http://lemonde.fr?Echobox=35272', 'lemonde.fr'),
    ('http://www2.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://m.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://mobile.lemonde.fr/index.html', 'lemonde.fr'),
    ('https://en.m.wikipedia.org/wiki/Ulam_spiral', 'en.wikipedia.org/wiki/Ulam_spiral'),
    ('http://lemonde.fr?XTOR=whatever', 'lemonde.fr'),
    ('http://lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4', 'lemonde.fr'),
    ('lemonde.fr?utm_hp_ref=test', 'lemonde.fr'),
    ('http://lemonde.fr?ref=fb', 'lemonde.fr'),
    ('http://lemonde.fr?ref=tw', 'lemonde.fr'),
    ('http://lemonde.fr?ref=tw_i', 'lemonde.fr'),
    ('http://lemonde.fr?platform=hootsuite', 'lemonde.fr'),
    ('lemonde.fr?__twitter_impression=true', 'lemonde.fr'),
    ('https://www4.lemonde.fr?een=34&seen=3458474', 'lemonde.fr'),
    ('https://www4.lemonde.fr?amp', 'lemonde.fr'),
    ('https://www4.lemonde.fr?amp_analytics=324', 'lemonde.fr'),
    ('http://lemonde.fr?fbclid=whatever', 'lemonde.fr')
]


class TestNormalizeUrl(object):
    def test_basics(self):
        for url, normalized in TESTS:
            assert normalize_url(url) == normalized, url

        assert normalize_url('lemonde.fr/index/', strip_trailing_slash=True) == 'lemonde.fr'
