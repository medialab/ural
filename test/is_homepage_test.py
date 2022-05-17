from ural import is_homepage

DEFAULT_TESTS = [
    ('https://www.example.com/foo/?bar=baz&inga=42&quux', False),
    ('http://www.outremers360.comtalent-de-la-semaine-la-designer-comorienne-aisha-wadaane-je-suis-fiere-de-mes-origines/', False),
    #('lemonde.fr/index.html', False),
    ('http://lemonde.fr///a/./b/..', False),
    #(u'http://例子.测试', True),
    #(u'http://مثال.إختبار', True),
    ('http://www.lemonde.fr', True),
]

class TestIsHomepage(object):
    def test_basics(self):
        for url, result in DEFAULT_TESTS:
            assert is_homepage(url) == result
