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
from ural.is_shortened_url import is_shortened_url


SHOULD_RESOLVE_DOMAINS = ['doi.org', 'list-manage.com']
SHOULD_RESOLVE_TRIE = HostnameTrieSet()

for domain in SHOULD_RESOLVE_DOMAINS:
    SHORTENER_DOMAINS_TRIE.add(domain)


def should_resolve(url):
    if is_homepage(url):
        return False

    if is_shortened_url(url):
        return True

    return SHOULD_RESOLVE_TRIE.match(url)
