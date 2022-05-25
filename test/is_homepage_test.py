from ural import is_homepage

DEFAULT_TESTS = [
    ("https://www.lemonde.fr/", True),
    ("https://www.lemonde.fr", True),
    ("https://www.lemonde.fr?hello=again", True),
    ("https://www.lemonde.fr#menu", True),
    ("lemonde.fr", True),
    ("https://www.lemonde.fr/resultats-elections/", False),
    ("http://business.lefigaro.fr/", True),
    ("https://www.lemonde.fr/index", True),
    ("https://www.lemonde.fr/index.html", True),
    ("https://www.lemonde.fr/index.html/", True),
    ("https://www.lemonde.fr/index.html/?hello", True),
    ("https://www.lemonde.fr/index.aspx", True),
    ("https://www.lemonde.fr/jokesindex", False),
    ("https://www.lemonde.fr/home", True),
    ("https://www.lemonde.fr/home.html", True),
    ("https://www.modulargrid.net/e/shakmat-modular-dual-dagger-", False)
]


class TestIsHomepage(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert is_homepage(url) == result
