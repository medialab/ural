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
from ural.utils import urljoin


def clean_link(link):
    """Removes leading and trailing whitespace and punctuation"""
    return link.strip("\t\r\n '\"\x0c")


def urls_from_html(string, base_url=None):
    """
    Function returning an iterator over the urls present in the HTML string argument.

    Args:
        string (str): source html string.
        base_url (str, optional): base_url to concatenate to the found urls.
            Defaults to None.

    Yields:
        str: an url.

    """
    for match in re.finditer(URL_IN_HTML_RE, string):
        url = clean_link(match.group(1))

        if base_url is not None:
            url = urljoin(base_url, url)

        yield url
