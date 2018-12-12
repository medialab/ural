#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Extraction Unit Tests
# =============================================================================
from ural import extract_urls

TEXT = """Facial-recognition technology is advancing faster than the people who worry about it have been able to think of ways to manage it." @NewYorker on the manifold challenges of harnessing a promising, but frightening, technology. http://mitsha.re/Qg1g30mVD78
Today @jovialjoy's @AJLUnited and @GeorgetownCPT are launching the Safe Face Pledge, which calls for facial analysis technology companies to commit to transparency in government contracts and mitigate potential abuse of their technology. http://www.safefacepledge.org  #safefacepledge
Now accepting submissions for the 2018 Excellence in Local News Awards http://twib.in/l/xLzxjnpMXx7X  via @medium http://foo.com/blah_(wikipedia)#cite-1
Directed to help #Alzheimers patients + others w/ impaired memory by providing intuitive ways to benefit from large amounts of personal data Check out this post by @physicspod in @singularityhub http://on.su.org/2rsPeXh"""


class TestStripProtocol(object):
    def test_basics(self):
        ref_set = set(["http://mitsha.re/Qg1g30mVD78",
                       "http://www.safefacepledge.org",
                       "http://twib.in/l/xLzxjnpMXx7X",
                       "http://on.su.org/2rsPeXh",
                       "http://foo.com/blah_(wikipedia)#cite-1"])
        result_set = set()
        for url in extract_urls(TEXT):
            result_set.add(url)
        assert result_set == ref_set
