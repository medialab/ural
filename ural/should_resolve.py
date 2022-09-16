# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Resolve Function
# =============================================================================
#
# Function testing whether the given url looks like something we should resolve.
#
from ural.tries import HostnameTrieSet
from ural.is_shortened_url import SHORTENER_DOMAINS_TRIE
from ural.is_homepage import is_homepage
from ural.utils import safe_urlsplit
import re


SHOULD_RESOLVE_DOMAINS = ['doi.org', 'list-manage.com']
SHOULD_RESOLVE_TRIE = HostnameTrieSet()

for domain in SHOULD_RESOLVE_DOMAINS:
    SHORTENER_DOMAINS_TRIE.add(domain)


def should_resolve(url):
    if is_homepage(url):
        return False

    if SHORTENER_DOMAINS_TRIE.match(url):
        return True

    url_split = safe_urlsplit(url)
    if url_split.hostname[:2] == 'l.' and re.fullmatch('/[0-9a-zA-Z]*', url_split.path) and not url_split.query and not url_split.fragment:
        return True

    return SHOULD_RESOLVE_TRIE.match(url)
