# -*- coding: utf-8 -*-
# =============================================================================
# Ural Could Be Html Unit Tests
# =============================================================================
from ural.could_be_html import could_be_html

TESTS = [
    ("lemonde.fr/article.html", True),
    ("https://www.lemonde.fr", True),
    ("lemonde.fr", True),
    ("https://www.lemonde.fr/", True),
    ("https://www.lemonde.fr/article.asp", True),
    ("https://www.lemonde.fr/article.php", True),
    ("https://www.lemonde.fr/article", True),
    ("https://www.lemonde.fr/article.json", False),
    ("https://www.lemonde.fr/article.xml", False),
    ("lemonde.fr/article.xml", False),
    ("lemonde.fr/article", True),
    ("https://www.lemonde.fr/img/figure.jpg", False),
    ("https://www.cosmopolitan.fr/inspirations-mode,2511387.asp1", True),
    ("https://www.cosmopolitan.fr/mode,2002.asp2", True),
]


class TestCouldBeHtml(object):
    def test_basics(self):
        for url, result in TESTS:
            assert could_be_html(url) == result, url
