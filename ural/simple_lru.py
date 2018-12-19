# =============================================================================
# Ural Simple LRU Function
# =============================================================================
#
# A function returning the url parts in the hierarchical order.
#
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol
from ural.normalize_url import normalize_url
from ural.patterns import IRRELEVANT_QUERY_COMBOS, IRRELEVANT_QUERY_RE, IRRELEVANT_SUBDOMAIN_RE


def attempt_to_decode_idna(string):
    try:
        return string.encode('utf8').decode('idna')
    except:
        return string


def simple_lru(url, strip_protocol=False, filter_subdomains=False, default_protocol='http'):
    full_url = ensure_protocol(url, protocol=default_protocol)
    scheme, netloc, path, query, fragment = normalize_url(full_url, strip_protocol=strip_protocol,
                                                          strip_irrelevant_subdomain=filter_subdomains, parsed=True)
    lru = []
    if urlsplit(url)[0]:
        lru.append('s:' + scheme)

    # Parsing domain & port
    netloc = netloc.split(':')
    if len(netloc) == 2:
        port = netloc[1]
        lru.append('t:' + port)
    for element in reversed(netloc[0].split('.')):
        lru.append('h:' + element)

    # Parsing the path
    for element in path.split('/'):
        if element:
            lru.append('p:' + element)
    if query and query[0]:
        for element in query.split('&'):
            lru.append('q:' + element)
    if fragment and fragment[0]:
        lru.append('f:' + fragment)

    return lru
