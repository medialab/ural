# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Typo URL Unit Tests
# =============================================================================
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
    (u'http://réélue.si', False),
    (u'http://beyoncé.com', False),
    ('https://www.instagram.com', False),
    ('http://mon.infolink.link/r/jdiz3yz', False),
    ('pharmacien.ne', True),
    ('forms.gle/EG2GpgRJea44DAbN7', False),
    ('http://dirigeants.es/', True),
    ('DIRIGEANTS.ES', True),
    ('triste.Il', True),
    ('site.Com', True),
    ('site.COM', False),
    ('site.cOM', True)
]


class TestIsTypoUrl(object):
    def test_basics(self):
        for url, result in TESTS:
            assert is_typo_url(url) == result
