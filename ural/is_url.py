# =============================================================================
# Ural URL Is URL Function
# =============================================================================
#
# A function returning True if its argument is a url.
#
import re
from ural.patterns import PROTOCOL_RE


def is_url(string, require_protocol=True):
    """
    Function returning True if its string argument is a url.

    Args:
        string (str): string to test.
        require_protocol (bool): whether the argument has to have a protocol to be considered a url. Is `True` by default.

    Returns:
        bool: True if the argument is a url, False if not.
    """
    PROTOCOL_URL_REGEX = r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
    URL_REGEX = r'^(?:(?:https?|ftp)://)?(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
    if require_protocol:
        pattern = re.compile(PROTOCOL_URL_REGEX)
    else:
        pattern = re.compile(URL_REGEX)
    if pattern.fullmatch(string):
        return True
    else:
        return False
