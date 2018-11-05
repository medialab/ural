# =============================================================================
# Ural URL Ensure Protocol Unit Tests
# =============================================================================
from ural import strip_protocol

TESTS = [
    ('http://lemonde.fr///a/./b/..', 'lemonde.fr///a/./b/..'),
    ('lemonde.fr/index.html', 'lemonde.fr/index.html'),
    ('lemonde.fr/index.php', 'lemonde.fr/index.php'),
    ('lemonde.fr/index/', 'lemonde.fr/index/'),
    ('lemonde.fr/index.php?utm_content=whatever&test=toto',
     'lemonde.fr/index.php?utm_content=whatever&test=toto'),
    ('lemonde.fr/index.php?utm_content=whatever',
     'lemonde.fr/index.php?utm_content=whatever'),
    ('https://lemonde.fr?', 'lemonde.fr?'),
    ('HTTPS://lemonde.fr?', 'lemonde.fr?'),
    ('https://lemonde.fr#anchor', 'lemonde.fr#anchor'),
    ('https://lemonde.fr/#anchor', 'lemonde.fr/#anchor'),
    ('https://lemonde.fr/#/path/is/here', 'lemonde.fr/#/path/is/here'),
    ('https://lemonde.fr#!/path/is/here', 'lemonde.fr#!/path/is/here'),
    ('//www.lemonde.fr', 'www.lemonde.fr'),
    ('http://www2.lemonde.fr/index.html', 'www2.lemonde.fr/index.html'),
    ('http://m.lemonde.fr/index.html', 'm.lemonde.fr/index.html'),
    ('http://mobile.lemonde.fr/index.html', 'mobile.lemonde.fr/index.html'),
    ('https://en.m.wikipedia.org/wiki/Ulam_spiral',
     'en.m.wikipedia.org/wiki/Ulam_spiral'),
    ('http://lemonde.fr?XTOR=whatever', 'lemonde.fr?XTOR=whatever'),
    ('http://lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4',
     'lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4'),
    ('lemonde.fr?utm_hp_ref=test', 'lemonde.fr?utm_hp_ref=test'),
    ('http://lemonde.fr?ref=fb', 'lemonde.fr?ref=fb'),
    ('http://lemonde.fr?ref=tw', 'lemonde.fr?ref=tw'),
    ('http://lemonde.fr?ref=tw_i', 'lemonde.fr?ref=tw_i'),
    ('http://lemonde.fr?platform=hootsuite',
     'lemonde.fr?platform=hootsuite'),
    ('lemonde.fr?__twitter_impression=true',
     'lemonde.fr?__twitter_impression=true'),
    ('https://www4.lemonde.fr?een=34&seen=3458474',
     'www4.lemonde.fr?een=34&seen=3458474'),
    ('https://www4.lemonde.fr?amp', 'www4.lemonde.fr?amp'),
    ('https://www4.lemonde.fr?amp_analytics=324',
     'www4.lemonde.fr?amp_analytics=324')
]


class TestStripProtocol(object):
    def test_basics(self):
        for url, output in TESTS:
            assert strip_protocol(url) == output
