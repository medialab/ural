# =============================================================================
# Ural Normalized LRU Function
# =============================================================================
#
# A function normalizing the url and returning its parts in the hierarchical order.
#
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol
from ural.normalize_url import normalize_url
from ural.patterns import IRRELEVANT_QUERY_COMBOS, IRRELEVANT_QUERY_RE, IRRELEVANT_SUBDOMAIN_RE


def normalized_lru(url, default_protocol='http', **kwargs):
    """
    Function normalizing the given url by stripping it of usually
    non-discriminant parts such as irrelevant query items or sub-domains, and
    returning its parts in the hierarchical order (lru).

    Args:
        url (str): Target URL as a string.
        sort_query (bool, optional): Whether to sort query items or not.
            Defaults to `True`.
        strip_authentication (bool, optional): Whether to drop authentication.
            Defaults to `True`.
        strip_trailing_slash (bool, optional): Whether to drop trailing slash.
            Defaults to `False`.
        strip_index (bool, optional): Whether to drop trailing index at the end
            of the url. Defaults to `True`.

    Returns:
        list: The normalized lru, with a prefix identifying the type of each part.
    """

    full_url = ensure_protocol(url, protocol=default_protocol)
    scheme, netloc, path, query, fragment = normalize_url(
        full_url, **kwargs, strip_protocol=False, parsed=True)
    lru = []
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
