# coding: utf-8
# =============================================================================
# Ural URL Fingerprinting Unit Tests
# =============================================================================
from __future__ import unicode_literals
from platform import python_version_tuple

PY2 = python_version_tuple()[0] == "2"


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


from ural import fingerprint_url

TESTS = [
    ("https://www.fr.lemonde.fr", "lemonde.fr"),
    ("https://www.fu.lemonde.fr", "fu.lemonde.fr"),
    ("https://www.fr-fu.lemonde.fr", "fr-fu.lemonde.fr"),
    ("https://www.french.lemonde.fr", "french.lemonde.fr"),
    ("https://www.french-fu.lemonde.fr", "french-fu.lemonde.fr"),
    ("https://www.fr-FR.lemonde.fr", "lemonde.fr"),
    ("https://www.lemonde.fr/path?gl=pt_BR&hl=fr", "lemonde.fr/path"),
    ("LEMONDE.FR/INDEX.HTML", "lemonde.fr"),
]


class TestFingerprintUrl(object):
    def test_fingerprint_url(self):
        for url, result in TESTS:
            assert fingerprint_url(url) == result
