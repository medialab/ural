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
        unquote,
        quote as original_quote
    )

    ALWAYS_SAFE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-~'

    def quote(string, safe='/'):
        if isinstance(string, unicode):
            safe_set = set(ord(c) for c in ALWAYS_SAFE)

            for c in safe:
                safe_set.add(ord(c))

            chars = [c if ord(c) in safe_set else '%{:02X}'.format(ord(c)) for c in string]

            return ''.join(chars)

        return original_quote(string, safe)

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
    urlpath = urlpath.strip()

    if not urlpath or urlpath == '/':
        return []

    urlpath = urlpath.strip('/')

    return urlpath.split('/')
