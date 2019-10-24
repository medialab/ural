# =============================================================================
# Ural LRU from URL Function
# =============================================================================
#
# A function returning the url parts in hierarchical order.
#
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol


def parsed_url_to_lru(parsed_url, tld_aware=False):
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


def lru_from_url(url, default_protocol='http', tld_aware=False):
    """
    Function returning the parts of the given url in the hierarchical order (lru).

    Args:
        url (str): Target URL as a string.
        default_protocol (str, optional): Protocol to add if there is none.
            Defaults to `'http'`.

    Returns:
        list: The lru, with a prefix identifying the type of each part.
    """

    full_url = ensure_protocol(url, protocol=default_protocol)
    return parsed_url_to_lru(urlsplit(full_url), tld_aware=tld_aware)
