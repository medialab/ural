# =============================================================================
# Ural URL Extraction Function
# =============================================================================
#
# A function returning an iterator over the urls present in the string argument.
#
import re
from ural.patterns import URL_IN_TEXT_RE


def urls_from_text(string):
    """
    Function returning an iterator over the urls present in the string argument.

    Args:
        string (str): source string.

    Yields:
        str: an url.

    """
    for url in re.finditer(URL_IN_TEXT_RE, string):
        yield url.group(0)
