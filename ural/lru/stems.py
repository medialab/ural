# =============================================================================
# Ural LRU Stems Function
# =============================================================================
#
# A function returning the url parts in hierarchical order.
#
from tld.utils import process_url
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol
from ural.normalize_url import normalize_url


def lru_stems_from_parse_url(parsed_url, tld_aware=True):
    scheme, netloc, path, query, fragment = parsed_url
    lru = []

    if scheme:
        lru.append('s:' + scheme)

    user = None
    password = None

    # Handling auth
    if '@' in netloc:
        auth, netloc = netloc.split('@', 1)

        if ':' in auth:
            user, password = auth.split(':', 1)
        else:
            user = auth

    # Parsing domain & port
    netloc = netloc.split(':', 1)

    if len(netloc) == 2:
        port = netloc[1]
        lru.append('t:' + port)

    # Need to process TLD?
    if tld_aware:
        domain_parts, non_zero_i, _ = process_url(
            url=parsed_url,
            fail_silently=True,
            fix_protocol=False,
            search_public=True,
            search_private=True
        )
        tld = '.'.join(domain_parts[non_zero_i:])
        lru.append('h:' + tld)
        for element in reversed(domain_parts[0:non_zero_i]):
            lru.append('h:' + element)

    else:
        for element in reversed(netloc[0].split('.')):
            lru.append('h:' + element)

    # Path
    for element in path.split('/')[1:]:
        lru.append('p:' + element)

    # Query
    if query and query[0]:
        lru.append('q:' + query)

    # Fragment
    if fragment and fragment[0]:
        lru.append('f:' + fragment)

    # User
    if user:
        lru.append('u:' + user)

    # Password
    if password:
        lru.append('w:' + password)
    return lru


# TODO: ensure_protocol
def lru_stems(url, tld_aware=False):
    """
    Function returning the parts of the given url in the hierarchical order (lru).

    Args:
        url (str): Target URL as a string.

    Returns:
        list: The lru, with a prefix identifying the type of each part.
    """

    full_url = ensure_protocol(url)
    return lru_stems_from_parse_url(urlsplit(full_url), tld_aware=tld_aware)


def normalized_lru_stems(url, tld_aware=False, **kwargs):
    full_url = ensure_protocol(url)
    parsed_url = normalize_url(full_url, parsed=True, **kwargs)
    return lru_stems_from_parse_url(parsed_url, tld_aware=tld_aware)
