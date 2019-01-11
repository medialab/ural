# =============================================================================
# Ural Normalized LRU from URL Function
# =============================================================================
#
# A function normalizing the url and returning its parts in the hierarchical order.
#
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol
from ural.lru_from_url import parsed_url_to_lru
from ural.normalize_url import normalize_url


def normalized_lru_from_url(url, default_protocol='http', **kwargs):
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
    return parsed_url_to_lru(normalize_url(
        full_url, parsed=True, **kwargs))
