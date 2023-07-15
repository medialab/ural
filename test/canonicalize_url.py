# coding: utf-8
# =============================================================================
# Ural URL Fingerprinting Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural import canonicalize_url

TESTS = [
    ("   http://lemonde.fr/test.html   ", "http://lemonde.fr/test.html"),
    ("http://lemonde.fr/test\x00.html", "http://lemonde.fr/test.html"),
    ("lemonde.fr", "https://lemonde.fr"),
    ("http://LEMONDE.FR/TEST", "http://lemonde.fr/TEST"),
    ("http://lemonde.fr:80/test", "http://lemonde.fr/test"),
    ("http://xn--tlrama-bvab.fr", "http://télérama.fr"),
    (
        "http://mozilla.org?x=%D1%88%D0%B5%D0%BB%D0%BB%D1%8B",
        "http://mozilla.org?x=шеллы",
    ),
    ("http://mozilla.org?x=шеллы", "http://mozilla.org?x=шеллы"),
]


class TestFingerprintUrl(object):
    def test_canonicalize_url(self):
        for url, result in TESTS:
            assert canonicalize_url(url) == result
