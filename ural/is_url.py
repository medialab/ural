# =============================================================================
# Ural URL Is URL Function
# =============================================================================
#
# A function returning True if its argument is a url.
#
from __future__ import unicode_literals
import re
from ural.patterns import PROTOCOL_RE

URL_REGEX = r'^([a-zA-Z0-9]*:?//)?(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'

protocol_pattern = re.compile(PROTOCOL_RE)
url_pattern = re.compile(URL_REGEX)


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
        return bool(protocol_pattern.match(string) and url_pattern.match(string))
    else:
        return bool(url_pattern.match(string))
