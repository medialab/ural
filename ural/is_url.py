# =============================================================================
# Ural URL Is URL Function
# =============================================================================
#
# A function returning True if its argument is a url.
#
import re
from ural.patterns import PROTOCOL_RE, URL_RE


def is_url(string, require_protocol=True):
    """
    Function returning True if its string argument is a url.

    Args:
        string (str): string to test.
        require_protocol (bool): whether the argument has to have a protocol to be considered a url. Is `True` by default.

    Returns:
        bool: True if the argument is a url, False if not.

    """

    if require_protocol:
        return bool(PROTOCOL_RE.match(string) and URL_RE.match(string))
    else:
        return bool(URL_RE.match(string))
