# =============================================================================
# Ural URL Extraction From HTML Function
# =============================================================================
#
# A function returning an iterator over the urls present in the HTML string
# argument.
#
from __future__ import unicode_literals
from ural.patterns import URL_IN_HTML_RE, URL_IN_HTML_BINARY_RE
from ural.utils import urljoin


def urls_finditer(string):
    for match in URL_IN_HTML_RE.finditer(string):
        url = match.group(1)

        if url is not None:
            url = url.strip('"')
        else:
            url = match.group(2)

            if url is not None:
                url = url.strip("'")
            else:
                url = match.group(3)

        assert url is not None

        yield url


def urls_finditer_binary(string, encoding="utf-8", errors="strict"):
    for match in URL_IN_HTML_BINARY_RE.finditer(string):
        url = match.group(1)

        if url is not None:
            url = url.strip(b'"')
        else:
            url = match.group(2)

            if url is not None:
                url = url.strip(b"'")
            else:
                url = match.group(3)

        assert url is not None

        yield url.decode(encoding, errors=errors)


def urls_from_html(string, base_url=None, encoding="utf-8", errors="strict"):
    """
    Function returning an iterator over the urls present in the HTML string argument.

    Args:
        string (str): source html string.
        base_url (str, optional): base_url to concatenate to the found urls.
            Defaults to None.

    Yields:
        str: an url.

    """
    iterator = (
        urls_finditer_binary(string, encoding=encoding, errors=errors)
        if isinstance(string, bytes)
        else urls_finditer(string)
    )

    for url in iterator:

        if base_url is not None:
            url = urljoin(base_url, url)

        yield url
