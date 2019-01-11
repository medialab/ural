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


def parsed_url_to_lru(parsed_url):
    scheme, netloc, path, query, fragment = parsed_url
    lru = []
    if scheme:
        lru.append('s:' + scheme)

    # Parsing domain & port
    netloc = netloc.split(':')
    if len(netloc) == 2:
        port = netloc[1]
        lru.append('t:' + port)
    for element in reversed(netloc[0].split('.')):
        lru.append('h:' + element)

    # Parsing the path
    for element in path.split('/')[1:]:
        lru.append('p:' + element)
    if query and query[0]:
        lru.append('q:' + query)
    if fragment and fragment[0]:
        lru.append('f:' + fragment)

    return lru


def lru_from_url(url, default_protocol='http'):
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
    return parsed_url_to_lru(urlsplit(full_url))
