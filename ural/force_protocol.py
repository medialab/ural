# =============================================================================
# Ural URL Force Protocol Function
# =============================================================================
#
# A function force-replacing the url protocol by the given one (and adding it if there is none).
#
import re

from ural.patterns import PROTOCOL_RE
from .strip_protocol import strip_protocol
from .ensure_protocol import ensure_protocol


def force_protocol(url, protocol='http'):
    """
    Function force-replacing the url protocol by the given one (and adding it if there is none).

    Args:
        url (str): Target URL as a string.
        protocol (str): protocol wanted. Is 'http' by default.

    Returns:
        string: The protocol-equipped url.

    """
    naked_url = strip_protocol(url)
    return ensure_protocol(naked_url, protocol)
