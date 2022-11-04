#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Extraction Unit Tests
# =============================================================================
from ural import urls_from_text

TEXT = """Facial-recognition technology is advancing faster than the people who worry about it have been able to think of ways to manage it." @NewYorker on the manifold challenges of harnessing a promising, but frightening, technology. http://mitsha.re/Qg1g30mVD78
Today @jovialjoy's @AJLUnited and @GeorgetownCPT are launching the Safe Face Pledge, which calls for facial analysis technology companies to commit to transparency in government contracts and mitigate potential abuse of their technology. http://www.safefacepledge.org  #safefacepledge
Now accepting submissions for the 2018 Excellence in Local News Awards http://twib.in/l/xLzxjnpMXx7X  via @medium http://foo.com/blah_(wikipedia)#cite-1
Directed to help #Alzheimers patients + others w/ impaired memory by providing intuitive ways to benefit from large amounts of personal data Check out this post by @physicspod in @singularityhub http://on.su.org/2rsPeXh"""

REF_SET = set(
    [
        "http://mitsha.re/Qg1g30mVD78",
        "http://www.safefacepledge.org",
        "http://twib.in/l/xLzxjnpMXx7X",
        "http://on.su.org/2rsPeXh",
        "http://foo.com/blah_(wikipedia)#cite-1",
    ]
)

TEXT_WITH_INVALID_URLS = """
This is a baaaad url: https://www.bfmtvregain-de-popularite-pour-emmanuel-macron-et-edouard-phi...
"""

TESTS = [
    (
        "please visit my website, https://oilab.eu/stijn, it's great",
        ["https://oilab.eu/stijn"],
    ),
    (
        "I recently read this in a new york times article (https://nytimes.com/some-url-with-(parentheses))",
        ["https://nytimes.com/some-url-with-(parentheses)"],
    ),
    (
        '"Bezoek alsjeblieft de websites van het [Juridisch Loket](https://www.juridischloket.nl/), [Sociaal Verhaal](http://www.sociaalverhaal.com/) en/of de [Rechtswinkel](http://www.rechtswinkel.nl/). Reddit is niet een geschikte plek voor juridisch advies."',
        [
            "https://www.juridischloket.nl/",
            "http://www.sociaalverhaal.com/",
            "http://www.rechtswinkel.nl/",
        ],
    ),
    (
        "What do you think of https://lemonde.fr? http://www.lemonde.fr. It is good http://www.lemonde.fr#?.",
        ["https://lemonde.fr", "http://www.lemonde.fr", "http://www.lemonde.fr"],
    ),
    (
        "This is: \"http://www.liberation.fr\" and 'https://lefigaro.fr'.",
        ["http://www.liberation.fr", "https://lefigaro.fr"],
    ),
    ("This is a [markdown]( https://lefigaro.fr) link.", ["https://lefigaro.fr"]),
    ("[http://www.lemonde.fr]", ["http://www.lemonde.fr"]),
]


class TestUrlsFromText(object):
    def test_basics(self):
        assert set(urls_from_text(TEXT)) == REF_SET

        for string, urls in TESTS:
            assert list(urls_from_text(string)) == urls

    def test_invalid_urls(self):
        urls = set(urls_from_text(TEXT_WITH_INVALID_URLS))

        assert urls == {"https://www.bfmtvregain"}
