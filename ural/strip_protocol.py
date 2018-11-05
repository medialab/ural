# =============================================================================
# Ural URL Ensure Protocol Function
# =============================================================================
#
# A function checking if the url features a protocol, and adding one if there is none.
#
import re

PROTOCOL_RE = re.compile('^[^:]*:?//')


def strip_protocol(url):
    """
    Function removing the protocol of the given url.

    Args:
        url (str): Target URL as a string.

    Returns:
        string: The url without protocol.

    """
    if PROTOCOL_RE.match(url):
        if url[:2] == '//':
            url = url[2:]
        else:
            url = url.split('://', 2)[1]
    return url
