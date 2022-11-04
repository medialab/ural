# =============================================================================
# Ural URL Ensure Protocol Function
# =============================================================================
#
# A function checking if the url has a protocol, and adding one if there is none.
#
from ural.patterns import PROTOCOL_RE


def ensure_protocol(url, protocol="http"):
    """
    Function checking if the url has a protocol, and adding the given one if there is none.

    Args:
        url (str): Target URL as a string.
        protocol (str): protocol to use if there is none in url. Is 'http' by default.

    Returns:
        string: The protocol-equipped url.

    """
    protocol = protocol.rstrip(":/")

    if not PROTOCOL_RE.match(url):
        url = protocol + "://" + url
    elif url.startswith("//"):
        url = protocol + ":" + url

    return url
