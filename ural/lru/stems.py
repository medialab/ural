# =============================================================================
# Ural LRU Stems Function
# =============================================================================
#
# A function returning the url parts in hierarchical order.
#
from tld.utils import process_url

from ural.utils import urlsplit
from ural.ensure_protocol import ensure_protocol
from ural.normalize_url import normalize_url


def lru_stems_from_parsed_url(parsed_url, tld_aware=True):
    scheme, _, path, query, fragment = parsed_url
    hostname = parsed_url.hostname or ''

    lru = []

    if scheme:
        lru.append('s:' + scheme)

    # Handling port
    if parsed_url.port is not None:
        lru.append('t:' + str(parsed_url.port))

    # Need to process TLD?
    should_process_normally = not tld_aware

    if tld_aware:
        domain_parts, non_zero_i, _ = process_url(
            url=parsed_url,
            fail_silently=True,
            fix_protocol=False,
            search_public=True,
            search_private=True
        )

        if domain_parts is None:
            should_process_normally = True

        else:
            tld = '.'.join(domain_parts[non_zero_i:])
            lru.append('h:' + tld)

            for element in reversed(domain_parts[0:non_zero_i]):
                lru.append('h:' + element)

    if should_process_normally:
        for element in reversed(hostname.split('.')):
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
    if parsed_url.username is not None:
        lru.append('u:' + parsed_url.username)

    # Password
    if parsed_url.password is not None:
        lru.append('w:' + parsed_url.password)

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
    return lru_stems_from_parsed_url(urlsplit(full_url), tld_aware=tld_aware)


def normalized_lru_stems(url, tld_aware=False, **kwargs):
    full_url = ensure_protocol(url)
    parsed_url = normalize_url(full_url, unsplit=False, **kwargs)
    return lru_stems_from_parsed_url(parsed_url, tld_aware=tld_aware)
