# =============================================================================
# Ural URL Extraction From HTML Function
# =============================================================================
#
# A function returning an iterator over the urls present in the HTML string
# argument.
#
from __future__ import unicode_literals
from ural.patterns import (
    URL_IN_HTML_RE,
    URL_IN_HTML_BINARY_RE,
    SCRIPT_TAG_RE,
    SCRIPT_TAG_BINARY_RE,
)

try:
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser

    _html_parser = HTMLParser()

    def unescape(string):
        return _html_parser.unescape(string)


def __urls_finditer(string):
    string = SCRIPT_TAG_RE.sub("", string)

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


def __urls_finditer_binary(string, encoding="utf-8", errors="strict"):
    string = SCRIPT_TAG_BINARY_RE.sub(b"", string)

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


def urls_from_html(string, encoding="utf-8", errors="strict"):
    if isinstance(string, bytes):
        iterator = __urls_finditer_binary(string, encoding=encoding, errors=errors)
    else:
        iterator = __urls_finditer(string)

    for url in iterator:
        url = url.strip()
        url = unescape(url)

        yield url
