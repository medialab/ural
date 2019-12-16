# =============================================================================
# Ural Various Utilities
# =============================================================================
#
# Miscellaneous utilities used throughout the library's code.
#
import re

from ural.patterns import PROTOCOL_RE

# PY2/PY3 compatible string_type...
string_type = str

try:
    string_type = basestring
except NameError:
    pass

# PY2/PY3 compatible urlparse
try:
    from urllib.parse import (
        parse_qs,
        parse_qsl,
        quote,
        unquote,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult
    )
except ImportError:
    from urllib import (
        quote,
        unquote
    )

    from urlparse import (
        parse_qs,
        parse_qsl,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult
    )


def safe_urlsplit(url, scheme='http'):
    if isinstance(url, SplitResult):
        return url

    if not re.match(PROTOCOL_RE, url):
        url = scheme + '://' + url

    splitted = urlsplit(url)

    return splitted


def urlpathsplit(urlpath):
    if urlpath == '/':
        return []

    urlpath = urlpath.strip('/')

    return urlpath.split('/')
