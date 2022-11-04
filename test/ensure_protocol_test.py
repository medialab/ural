# =============================================================================
# Ural URL Ensure Protocol Unit Tests
# =============================================================================
from ural import ensure_protocol

TESTS = [
    ("http://lemonde.fr///a/./b/..", "http://lemonde.fr///a/./b/.."),
    ("lemonde.fr/index.html", "http://lemonde.fr/index.html"),
    ("lemonde.fr/index.php", "http://lemonde.fr/index.php"),
    ("lemonde.fr/index/", "http://lemonde.fr/index/"),
    (
        "lemonde.fr/index.php?utm_content=whatever&test=toto",
        "http://lemonde.fr/index.php?utm_content=whatever&test=toto",
    ),
    (
        "lemonde.fr/index.php?utm_content=whatever",
        "http://lemonde.fr/index.php?utm_content=whatever",
    ),
    ("https://lemonde.fr?", "https://lemonde.fr?"),
    ("https://lemonde.fr#anchor", "https://lemonde.fr#anchor"),
    ("https://lemonde.fr/#anchor", "https://lemonde.fr/#anchor"),
    ("https://lemonde.fr/#/path/is/here", "https://lemonde.fr/#/path/is/here"),
    ("https://lemonde.fr#!/path/is/here", "https://lemonde.fr#!/path/is/here"),
    ("//www.lemonde.fr", "http://www.lemonde.fr"),
    ("http://www2.lemonde.fr/index.html", "http://www2.lemonde.fr/index.html"),
    ("http://m.lemonde.fr/index.html", "http://m.lemonde.fr/index.html"),
    ("http://mobile.lemonde.fr/index.html", "http://mobile.lemonde.fr/index.html"),
    (
        "https://en.m.wikipedia.org/wiki/Ulam_spiral",
        "https://en.m.wikipedia.org/wiki/Ulam_spiral",
    ),
    ("http://lemonde.fr?XTOR=whatever", "http://lemonde.fr?XTOR=whatever"),
    (
        "http://lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4",
        "http://lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4",
    ),
    ("lemonde.fr?utm_hp_ref=test", "http://lemonde.fr?utm_hp_ref=test"),
    ("http://lemonde.fr?ref=fb", "http://lemonde.fr?ref=fb"),
    ("http://lemonde.fr?ref=tw", "http://lemonde.fr?ref=tw"),
    ("http://lemonde.fr?ref=tw_i", "http://lemonde.fr?ref=tw_i"),
    ("http://lemonde.fr?platform=hootsuite", "http://lemonde.fr?platform=hootsuite"),
    (
        "lemonde.fr?__twitter_impression=true",
        "http://lemonde.fr?__twitter_impression=true",
    ),
    (
        "https://www4.lemonde.fr?een=34&seen=3458474",
        "https://www4.lemonde.fr?een=34&seen=3458474",
    ),
    ("https://www4.lemonde.fr?amp", "https://www4.lemonde.fr?amp"),
    (
        "https://www4.lemonde.fr?amp_analytics=324",
        "https://www4.lemonde.fr?amp_analytics=324",
    ),
]


class TestEnsureProtocol(object):
    def test_basics(self):
        for url, output in TESTS:
            assert ensure_protocol(url) == output
        assert (
            ensure_protocol("lemonde.fr?utm_hp_ref=test", "ftp")
            == "ftp://lemonde.fr?utm_hp_ref=test"
        )
        assert (
            ensure_protocol("https://lemonde.fr?utm_hp_ref=test", "ftp")
            == "https://lemonde.fr?utm_hp_ref=test"
        )
        assert (
            ensure_protocol("lemonde.fr?utm_hp_ref=test", "http://")
            == "http://lemonde.fr?utm_hp_ref=test"
        )
