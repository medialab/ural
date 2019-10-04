# =============================================================================
# Ural URL Strip Protocol Function
# =============================================================================
#
# A function removing the protocol from the given url.
#
from ural.patterns import PROTOCOL_RE


def strip_protocol(url):
    """
    Function removing the protocol from the given url.

    Args:
        url (str): Target URL as a string.

    Returns:
        string: The url without protocol.

    """
    return PROTOCOL_RE.sub("", url)
