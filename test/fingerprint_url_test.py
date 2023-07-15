# coding: utf-8
# =============================================================================
# Ural URL Fingerprinting Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural import fingerprint_url, fingerprint_hostname

TESTS = [
    ("https://www.fr.lemonde.fr", "lemonde.fr"),
    ("https://www.fu.lemonde.fr", "fu.lemonde.fr"),
    ("https://www.fr-fu.lemonde.fr", "fr-fu.lemonde.fr"),
    ("https://www.french.lemonde.fr", "french.lemonde.fr"),
    ("https://www.french-fu.lemonde.fr", "french-fu.lemonde.fr"),
    ("https://www.fr-FR.lemonde.fr", "lemonde.fr"),
    ("https://www.lemonde.fr/path?gl=pt_BR&hl=fr", "lemonde.fr/path"),
    ("LEMONDE.FR/INDEX.HTML", "lemonde.fr"),
    ("lemonde.fr:6754", "lemonde.fr"),
]


class TestFingerprintUrl(object):
    def test_fingerprint_url(self):
        for url, result in TESTS:
            assert fingerprint_url(url) == result

    def test_fingerprint_hostname(self):
        assert fingerprint_hostname("fr.lemonde.fr") == "lemonde.fr"
