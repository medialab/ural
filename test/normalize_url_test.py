# coding: utf-8
# =============================================================================
# Ural URL Normalization Unit Tests
# =============================================================================
from ural import normalize_url, get_normalized_hostname, get_hostname

TESTS = [
    ('http://lemonde.fr///a/./b/..', 'lemonde.fr/a'),
    ('lemonde.fr/index.html', 'lemonde.fr'),
    ('lemonde.fr/index.php', 'lemonde.fr'),
    ('lemonde.fr/index.php?utm_content=whatever&test=toto', 'lemonde.fr?test=toto'),
    ('lemonde.fr/index.php?utm_content=whatever', 'lemonde.fr'),
    ('https://lemonde.fr?', 'lemonde.fr'),
    ('https://lemonde.fr#anchor', 'lemonde.fr'),
    ('https://lemonde.fr/#anchor', 'lemonde.fr'),
    ('https://lemonde.fr/#/path/is/here', 'lemonde.fr/#/path/is/here'),
    ('https://lemonde.fr#!/path/is/here', 'lemonde.fr#!/path/is/here'),
    ('//www.lemonde.fr', 'lemonde.fr'),
    ('//www.lemonde.fr?XTOR=whatev', 'lemonde.fr'),
    ('http://lemonde.fr?Echobox=35272', 'lemonde.fr'),
    ('http://www2.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://m.lemonde.fr/index.html', 'lemonde.fr'),
    ('http://mobile.lemonde.fr/index.html', 'lemonde.fr'),
    ('https://en.m.wikipedia.org/wiki/Ulam_spiral', 'en.wikipedia.org/wiki/Ulam_spiral'),
    ('http://lemonde.fr?XTOR=whatever', 'lemonde.fr'),
    ('http://lemonde.fr?xtref=1&xtcr=2&xts=3&xtnp=3&xtloc=4', 'lemonde.fr'),
    ('lemonde.fr?utm_hp_ref=test', 'lemonde.fr'),
    ('http://lemonde.fr?ref=fb', 'lemonde.fr'),
    ('http://lemonde.fr?ref=tw', 'lemonde.fr'),
    ('http://lemonde.fr?ref=tw_i', 'lemonde.fr'),
    ('http://lemonde.fr?platform=hootsuite', 'lemonde.fr'),
    ('lemonde.fr?__twitter_impression=true', 'lemonde.fr'),
    ('https://www4.lemonde.fr?een=34&seen=3458474', 'lemonde.fr'),
    ('https://www4.lemonde.fr?amp', 'lemonde.fr'),
    ('https://www4.lemonde.fr?amp_analytics=324', 'lemonde.fr'),
    ('http://lemonde.fr?fbclid=whatever', 'lemonde.fr'),
    ('http://xn--tlrama-bvab.fr', u'télérama.fr'),
    ('http://www.lemonde.fr?page=2&id=3', 'lemonde.fr?id=3&page=2'),
    ('WWW.LEMONDE.FR', 'lemonde.fr'),
    ('https://lemonde.fr#', 'lemonde.fr'),
    ('https://yomgui:mdp@lemonde.fr', 'lemonde.fr'),
    ('https://yomgui@lemonde.fr', 'lemonde.fr'),
    ('http://lemonde.fr:80', 'lemonde.fr'),
    ('https://lemonde.fr:443', 'lemonde.fr'),
    ('https://lemonde.fr?ref=ts&fref=ts', 'lemonde.fr'),
    ('https://lemonde.fr?utm_source&utm_medium&utm_campaign', 'lemonde.fr'),
    ('http://www.europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641.amp', 'europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641'),
    ('http://www.sciencesetavenir.fr/fondamental/journee-mondiale-du-bonheur-le-secret-pour-etre-heureux-selon-albert-einstein_117633.amp?__twitter_impression=true', 'sciencesetavenir.fr/fondamental/journee-mondiale-du-bonheur-le-secret-pour-etre-heureux-selon-albert-einstein_117633'),
    ('http://www.sudouest.fr/2017/08/15/un-an-ferme-pour-avoir-frappe-des-gendarmesle-dimanche-moins-frequente-3696402-3350.amp.html', 'sudouest.fr/2017/08/15/un-an-ferme-pour-avoir-frappe-des-gendarmesle-dimanche-moins-frequente-3696402-3350.html'),
    ('http://newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/amp', 'newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/'),
    ('http://newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/amp/', 'newsinfo.inquirer.net/900478/maute-gunmen-in-their-teens/'),
    ('https://fr.aleteia.org/2018/07/17/lhonnetete-de-huit-jeunes-garcons-recompensee/amp/?__twitter_impression=true', 'fr.aleteia.org/2018/07/17/lhonnetete-de-huit-jeunes-garcons-recompensee/'),
    ('http://amp.lefigaro.fr/actualite-france/les-geysers-de-rue-redoublent-avec-la-canicule-20190628', 'lefigaro.fr/actualite-france/les-geysers-de-rue-redoublent-avec-la-canicule-20190628'),
    ('http://mashable-com.cdn.ampproject.org/c/s/mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp', 'mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing'),
    ('http://www.europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641.amp/', 'europe1.fr/sante/les-onze-vaccins-obligatoires-pour-les-enfants-a-partir-du-1er-janvier-3423641'),
    ('http://amp-madame.lefigaro.fr/bien-etre/carla-bruni-et-cynthia-fleury-lamour-construit-letre-et-la-societe-141214-93346', 'madame.lefigaro.fr/bien-etre/carla-bruni-et-cynthia-fleury-lamour-construit-letre-et-la-societe-141214-93346'),
    ('http://pluzz.francetv.fr/videos/jt_1920_champagne_ardenne.html#xtref=https://www.google.fr/', 'pluzz.francetv.fr/videos/jt_1920_champagne_ardenne.html'),
    ('https://ohioamf.org]', 'https://ohioamf.org]'),
    ('https://lemonde.fr/test#/', 'lemonde.fr/test'),
    ('https://lemonde.fr/test#!/', 'lemonde.fr/test'),
    ('https://lemonde.fr/test#!', 'lemonde.fr/test'),
    ('http://lemonde.fr/test#xtor=RSS-11', 'lemonde.fr/test'),
    ('http://m.youtube.com/watch?v=X2gSGCOVaZk&feature=youtu.be', 'youtube.com/watch?v=X2gSGCOVaZk'),
    ('https://www.instagram.com/wondher/?utm_source=ig_profile_share&igshid=if58b3qro9yw', 'instagram.com/wondher/'),
    ('https://www.change.org/p/ville-de-saint-malo-electrik-parade-saint-malo?recruiter=797274685&utm_source=share_petition&utm_medium=twitter&utm_campaign=share_petition&utm_term=autopublish&utm_content=nafta_twitter_large_image_card%3Areal_control', 'change.org/p/ville-de-saint-malo-electrik-parade-saint-malo'),
    ('http://bazaistoria.ru/blog/43285809262/Britanskaya-diplomatiya.-CHto-za-zver?utm_campaign=transit&amp;utm_source=main&amp;utm_medium=page_0&amp;domain=mirtesen.ru&amp;paid=1&amp;pad=1', 'bazaistoria.ru/blog/43285809262/Britanskaya-diplomatiya.-CHto-za-zver?domain=mirtesen.ru&pad=1&paid=1'),
    ('http://mozilla.org?x=шеллы', 'mozilla.org?x=%D1%88%D0%B5%D0%BB%D0%BB%D1%8B'),
    ('https://facebook.com/kaliwakatee?refid=52&__tn__=R', 'facebook.com/kaliwakatee'),
    ('http://www.wired.co.uk/magazine/archive/2012/11/features/open-university?fb_source=feed&ref=feed&refid=28&_ft_=qid.5811242880099719698:mf_story_key.371116929646636', 'wired.co.uk/magazine/archive/2012/11/features/open-university')
]


TESTS_ADVANCED = [
    ('lemonde.fr/index/', 'lemonde.fr', {'strip_trailing_slash': True}),
    ('https://yomgui@lemonde.fr', 'yomgui@lemonde.fr', {'strip_authentication': False}),
    ('https://www.lemonde.fr', 'https://www.lemonde.fr', {"strip_protocol": False, "strip_irrelevant_subdomain": False}),
    ('www.lemonde.fr', 'www.lemonde.fr', {"strip_protocol": False, "strip_irrelevant_subdomain": False}),
    ('https://www.fr.lemonde.fr', 'lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.fu.lemonde.fr', 'fu.lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.fr-fu.lemonde.fr', 'fr-fu.lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.french.lemonde.fr', 'french.lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.french-fu.lemonde.fr', 'french-fu.lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.fr-FR.lemonde.fr', 'lemonde.fr', {"strip_lang_subdomains": True}),
    ('https://www.lemonde.fr#test', 'lemonde.fr#test', {"strip_fragment": False}),
    ('https://www.lemonde.fr#/path', 'lemonde.fr#/path', {"strip_fragment": False}),
    ('https://www.lemonde.fr#test', 'lemonde.fr', {"strip_fragment": True}),
    ('https://www.lemonde.fr#/path', 'lemonde.fr', {"strip_fragment": True}),
    ('https://www.lemonde.fr#test', 'lemonde.fr', {"strip_fragment": 'except-routing'}),
    ('https://www.lemonde.fr#/path', 'lemonde.fr#/path', {"strip_fragment": 'except-routing'}),
    (
        'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=2ahUKEwjp8Lih_LnmAhWQlxQKHVTmCJYQFjADegQIARAB&url=http%3A%2F%2Fwww.mon-ip.com%2F&usg=AOvVaw0sfeZJyVtUS2smoyMlJmes',
        'mon-ip.com',
        {'resolve_obvious_redirects': True}
    ),
    (
        'http://mozilla.org?x=шеллы',
        'mozilla.org?x=шеллы',
        {'quoted': False}
    ),
    (
        'http://mozilla.org?x=%D1%88%D0%B5%D0%BB%D0%BB%D1%8B',
        'mozilla.org?x=шеллы',
        {'quoted': False}
    ),
    (
        'https://www.lemonde.fr/path?gl=pt_BR&hl=fr',
        'lemonde.fr/path',
        {'strip_lang_query_items': True}
    )
]


class TestNormalizeUrl(object):
    def test_normalize_url(self):
        for url, normalized in TESTS:
            assert normalize_url(url) == normalized, url

        for url, normalized, kwargs in TESTS_ADVANCED:
            assert normalize_url(url, **kwargs) == normalized, url

    def test_get_normalized_hostname(self):
        for url, normalized in TESTS:
            assert get_normalized_hostname(url) == get_hostname(normalized)

        for url, normalized, kwargs in TESTS_ADVANCED:
            if 'strip_lang_subdomains' not in kwargs:
                continue

            assert get_normalized_hostname(url, **kwargs) == get_hostname(normalized)
