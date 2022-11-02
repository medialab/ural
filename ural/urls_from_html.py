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
from ural.is_url import is_url


def clean_link(link):
    """Removes leading and trailing whitespace and punctuation"""
    return link.strip("\t\r\n '\"\x0c")


def urls_from_html(string, base_url=''):
    """
    Function returning an iterator over the urls present in the HTML string argument.

    Args:
        string (str): source html string.
        base_url (str, optional): base_url to concatenate to the found urls. Defaults to empty string.

    Yields:
        str: an url.

    """
    for match in re.finditer(URL_IN_HTML_RE, string):
        url = clean_link(match.group(1))

        if not is_url(url):
            url = base_url + url

        yield url
