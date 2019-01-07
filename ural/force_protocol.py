# =============================================================================
# Ural URL Force Protocol Function
# =============================================================================
#
# A function force-replacing the url protocol by the given one (and adding it if there is none).
#
import re

from ural.patterns import PROTOCOL_RE


def force_protocol(url, protocol='http'):
    """
    Function force-replacing the url protocol by the given one (and adding it if there is none).

    Args:
        url (str): Target URL as a string.
        protocol (str): protocol wanted. Is 'http' by default.

    Returns:
        string: The protocol-equipped url.

    """
    protocol = protocol.rstrip(':/')

    if not PROTOCOL_RE.match(url):
        url = protocol + '://' + url
    elif url[:2] == '//':
        url = protocol + ':' + url
    else:
        url = re.sub(PROTOCOL_RE, protocol + '://', url)

    return url
