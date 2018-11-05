# =============================================================================
# Ural URL Ensure Protocol Function
# =============================================================================
#
# A function checking if the url features a protocol, and adding one if there is none.
#
import re

PROTOCOL_RE = re.compile(r'^[^:]*:?//')


def ensure_protocol(url, protocol='http'):
    """
    Function checking if the url features a protocol, and adding the given one if there is none.

    Args:
        url (str): Target URL as a string.
        protocol (str): protocol to use if there is none in url. Is 'http' by default.

    Returns:
        string: The protocol-equipped url.

    """
    if not PROTOCOL_RE.match(url):
        url = protocol + '://' + url
    elif url[:2] == '//':
        url = protocol + ':' + url
    return url
