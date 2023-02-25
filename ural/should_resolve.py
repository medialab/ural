# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Resolve Function
# =============================================================================
#
# Function testing whether the given url looks like something we should resolve.
#
from ural.classes.hostname_trie_set import HostnameTrieSet
from ural.is_shortened_url import SHORTENER_DOMAINS, is_l_shortened_domain
from ural.is_homepage import is_homepage
from ural.utils import safe_urlsplit

SHOULD_RESOLVE_DOMAINS = ["doi.org", "list-manage.com"]
SHOULD_RESOLVE_TRIE = HostnameTrieSet()

for domain in SHORTENER_DOMAINS + SHOULD_RESOLVE_DOMAINS:
    SHOULD_RESOLVE_TRIE.add(domain)


def should_resolve(url):
    parsed = safe_urlsplit(url)

    # NOTE: shortener domain homepages are not shortened urls per se
    if is_homepage(parsed):
        return False

    # Shortener domains starting with 'l.'
    if is_l_shortened_domain(parsed):
        return True

    return SHOULD_RESOLVE_TRIE.match(parsed)
