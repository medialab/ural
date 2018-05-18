# =============================================================================
# Ural URL Normalization Unit Tests
# =============================================================================
from ural import normalize_url

TESTS = [
    ('http://lemonde.fr///a/./b/..', 'lemonde.fr/a'),
    ('lemonde.fr/index.html', 'lemonde.fr'),
    ('lemonde.fr/index.php', 'lemonde.fr'),
    ('lemonde.fr/index/', 'lemonde.fr'),
    ('lemonde.fr/index.php?utm_content=whatever&test=toto', 'lemonde.fr?test=toto'),
    ('lemonde.fr/index.php?utm_content=whatever', 'lemonde.fr'),
    ('https://lemonde.fr?', 'lemonde.fr'),
    ('https://lemonde.fr#anchor', 'lemonde.fr'),
    ('https://lemonde.fr/#anchor', 'lemonde.fr'),
    ('https://lemonde.fr/#/path/is/here', 'lemonde.fr/#/path/is/here'),
    ('https://lemonde.fr#!/path/is/here', 'lemonde.fr#!/path/is/here'),
    ('//www.lemonde.fr', 'lemonde.fr'),
    ('http://www2.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://m.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://mobile.lemonde.fr/index.html', 'lemonde.fr')
]


class TestNormalizeUrl(object):
    def test_basics(self):
        for url, normalized in TESTS:
            assert normalize_url(url) == normalized
