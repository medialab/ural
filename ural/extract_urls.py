# =============================================================================
# Ural URL Extraction Function
# =============================================================================
#
# A function returning an iterator over the urls present in the string argument.
#
from __future__ import unicode_literals
import re
from ural.patterns import URL_IN_TEXT_RE


def extract_urls(string):
    """
    Function returning an iterator over the urls present in the string argument.

    Args:
        string (str): source string.

    Returns:
        iterator: an iterator on the urls present in the string argument.
    """
    for url in re.finditer(URL_IN_TEXT_RE, string):
        yield url.group(0)
