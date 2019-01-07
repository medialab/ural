from __future__ import unicode_literals
import re

PROTOCOL_RE = re.compile(r'^[a-zA-Z0-9]*:?//')

URL_RE_BASE = r"(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"

URL_RE = re.compile(
    r'^([a-zA-Z0-9]*:?//)?%s$' % URL_RE_BASE)

URL_IN_TEXT_RE = re.compile(
    r'([a-zA-Z0-9]*:?//)%s' % URL_RE_BASE)

HTML_URL_RE = re.compile(
    r"<a\s.*?href=(?:\"([.#]+?)\"|\'([.#]+?)\'|([^\s]+?))(?:>|\s.*?>)(?:.*?)<[/ ]?a>",
    re.DOTALL | re.IGNORECASE)

IRRELEVANT_QUERY_RE = re.compile(
    r'^(?:__twitter_impression|echobox|fbclid|utm_.+|amp_.+|amp|s?een|xt(?:loc|ref|cr|np|or|s))$', re.I)

IRRELEVANT_SUBDOMAIN_RE = re.compile(r'\b(?:www\d?|mobile|m)\.', re.I)

IRRELEVANT_QUERY_COMBOS = {
    'ref': ('fb', 'tw', 'tw_i'),
    'platform': ('hootsuite')
}
