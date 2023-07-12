# =============================================================================
# Ural LRU Stems Function
# =============================================================================
#
# A function returning the url parts in hierarchical order.
#
import re

from ural.utils import urlsplit
from ural.tld import split_suffix
from ural.ensure_protocol import ensure_protocol
from ural.normalize_url import normalize_url
from ural.has_special_host import is_special_host

PORT_SPLITTER = re.compile(r":(?![\d:]+])")


def lru_stems_from_parsed_url(parsed_url, suffix_aware=True):
    scheme, netloc, path, query, fragment = parsed_url
    lru = []

    if scheme:
        lru.append("s:" + scheme)

    user = None
    password = None

    # Handling auth
    if "@" in netloc:
        auth, netloc = netloc.split("@", 1)

        if ":" in auth:
            user, password = auth.split(":", 1)
        else:
            user = auth

    # Parsing domain & port
    netloc = PORT_SPLITTER.split(netloc)

    if len(netloc) == 2:
        port = netloc[1]
        lru.append("t:" + port)

    # Need to process TLD?
    should_process_normally = not suffix_aware

    if suffix_aware:
        split_result = split_suffix(parsed_url)

        if split_result is None:
            should_process_normally = True

        else:
            domain, suffix = split_result
            lru.append("h:" + suffix)

            if domain:
                for element in reversed(domain.split(".")):
                    lru.append("h:" + element)

    if should_process_normally:
        if is_special_host(netloc[0]):
            lru.append("h:" + netloc[0])
        else:
            for element in reversed(netloc[0].split(".")):
                lru.append("h:" + element)

    # Path
    for element in path.split("/")[1:]:
        lru.append("p:" + element)

    # Query
    if query and query[0]:
        lru.append("q:" + query)

    # Fragment
    if fragment and fragment[0]:
        lru.append("f:" + fragment)

    # User
    if user:
        lru.append("u:" + user)

    # Password
    if password:
        lru.append("w:" + password)
    return lru


# TODO: ensure_protocol
def lru_stems(url, suffix_aware=False):
    """
    Function returning the parts of the given url in the hierarchical order (lru).

    Args:
        url (str): Target URL as a string.

    Returns:
        list: The lru, with a prefix identifying the type of each part.
    """

    full_url = ensure_protocol(url)
    return lru_stems_from_parsed_url(urlsplit(full_url), suffix_aware=suffix_aware)


def normalized_lru_stems(url, suffix_aware=False, **kwargs):
    full_url = ensure_protocol(url)
    parsed_url = normalize_url(full_url, unsplit=False, **kwargs)
    return lru_stems_from_parsed_url(parsed_url, suffix_aware=suffix_aware)
