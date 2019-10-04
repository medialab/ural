# =============================================================================
# Ural URL Extraction From HTML Function
# =============================================================================
#
# A function returning an iterator over the urls present in the HTML string
# argument.
#
from __future__ import unicode_literals
import re
from ural.patterns import URL_IN_HTML_RE


def clean_link(link):
    """Removes leading and trailing whitespace and punctuation"""
    return link.strip("\t\r\n '\"\x0c")


def urls_from_html(string):
    """
    Function returning an iterator over the urls present in the HTML string argument.

    Args:
        string (str): source html string.

    Yields:
        str: an url.

    """
    for a_tag in re.finditer(URL_IN_HTML_RE, string):
        url = a_tag.group(3)
        yield clean_link(url)
