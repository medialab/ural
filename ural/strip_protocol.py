# =============================================================================
# Ural URL Strip Protocol Function
# =============================================================================
#
# A function removing the protocol from the given url.
#
import re
from .normalize_url import PROTOCOL_RE

# PROTOCOL_RE = re.compile(r'^[^:]*:?//')


def strip_protocol(url):
    """
    Function removing the protocol from the given url.

    Args:
        url (str): Target URL as a string.

    Returns:
        string: The url without protocol.

    """
    return PROTOCOL_RE.sub("", url)
