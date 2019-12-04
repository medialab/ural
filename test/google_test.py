# =============================================================================
# Ural Youtube Unit Tests
# =============================================================================
import pytest
from ural.google import (
    is_amp_url
)

IS_AMP_TESTS = [
    ('https://lemonde.fr#', False),
    ('https://yomgui:mdp@lemonde.fr', False),
    ('https://yomgui@lemonde.fr', False),
    ('http://lemonde.fr:80', False),
    ('https://lemonde.fr:443', False),
    ('https://lemonde.fr?ref=ts&fref=ts', False),
    ('https://lemonde.fr?utm_source&utm_medium&utm_campaign', False),
    ('http://www.europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641.amp', True),
    ('http://www.sciencesetavenir.fr/fondamental/journee-mondiale-du-bonheur-le-secret-pour-etre-heureux-selon-albert-einstein_117633.amp?__twitter_impression=true', True),
    ('http://www.sudouest.fr/2017/08/15/un-an-ferme-pour-avoir-frappe-des-gendarmesle-dimanche-moins-frequente-3696402-3350.amp.html', True),
    ('http://newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/amp', True),
    ('http://newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/amp/', True),
    ('https://fr.aleteia.org/2018/07/17/lhonnetete-de-huit-jeunes-garcons-recompensee/amp/?__twitter_impression=true', True),
    ('http://amp.lefigaro.fr/actualite-france/les-geysers-de-rue-redoublent-avec-la-canicule-20190628', True),
    ('http://mashable-com.cdn.ampproject.org/c/s/mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp', True),
    ('http://www.europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641.amp/', True),
    ('http://amp-madame.lefigaro.fr/bien-etre/carla-bruni-et-cynthia-fleury-lamour-construit-letre-et-la-societe-141214-93346', True),
    ('http://pluzz.francetv.fr/videos/jt_1920_champagne_ardenne.html#xtref=https://www.google.fr/', False),
    ('http://indystar.com/amp/551071002', True)
]


class TestGoogle(object):
    def test_is_amp_url(self):
        for url, result in IS_AMP_TESTS:
            assert is_amp_url(url) == result
