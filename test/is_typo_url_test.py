# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Typo URL Unit Tests
# =============================================================================
from __future__ import unicode_literals
from ural import is_typo_url

TESTS = [
    ('http://nombreux.se', True),
    ('http://10.37.42.04.dvr', True),
    ('http://france.plus', True),
    ('http://anxieu.x.se', True),
    ('http://dirigeants.es', True),
    ('http://designandhuman.com-labo.mg', True),
    ('http://www.membres.republicains.fr/rentreejr', False),
    ('http://www.livreblanc.urbassist.fr', False),
    ('https://apmnews.com/story.php?objet=370495', False),
    ('https://univ-paris8.fr/La-vaccination', False),
    ('http://réélue.si', False),
    ('http://beyoncé.com', False),
    ('https://www.instagram.com', False),
    ('http://mon.infolink.link/r/jdiz3yz', False),
    ('pharmacien.ne', True),
    ('forms.gle/EG2GpgRJea44DAbN7', False),
    ('http://dirigeants.es/', True),
    ('DIRIGEANTS.ES', True),
    ('triste.Il', True),
    ('site.Com', True),
    ('site.COM', False),
    ('site.cOM', True),
    ('https://transilien.com#icv-P-6efefc31-f418-45e4-a6dc-f93567a79ac7', False),
    ('https://www.gaiff.am', False),
    ('http://username:password@www.my_site.com', False),
    ('http://user@name:pass@word@www.my_site.com', False),
]


class TestIsTypoUrl(object):
    def test_basics(self):
        for url, result in TESTS:
            assert is_typo_url(url) == result
