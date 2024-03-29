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
        quote,
        unquote,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult,
    )
except ImportError:
    from urllib import unquote, quote as original_quote

    def quote(string, safe="/"):
        if isinstance(string, unicode):
            return original_quote(string.encode("utf-8"), safe)

        return original_quote(string, safe)

    from urlparse import (
        parse_qs,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult,
    )

MISTAKES_RE = re.compile(r"&amp(?:%3B|;)", re.I)

# NOTE: one of the kwargs below is not so aptly named quote...
unshadowed_quote = quote


def safe_urlsplit(url, scheme="http"):
    if isinstance(url, SplitResult):
        return url

    if not re.match(PROTOCOL_RE, url):
        url = scheme + "://" + url

    splitted = urlsplit(url)

    return splitted


def pathsplit(urlpath):
    urlpath = urlpath.strip()

    if not urlpath or urlpath == "/":
        return []

    urlpath = urlpath.strip("/")

    return urlpath.split("/")


def urlpathsplit(url):
    parsed = safe_urlsplit(url)
    return pathsplit(parsed.path)


SLASH_SQUEEZE_RE = re.compile(r"\/{2,}")


def normpath(urlpath, drop_consecutive_slashes=True):
    if drop_consecutive_slashes:
        urlpath = SLASH_SQUEEZE_RE.sub("/", urlpath)

    segments = urlpath.split("/")
    segments = [segment + "/" for segment in segments[:-1]] + [segments[-1]]
    resolved = []

    for segment in segments:
        if segment in ("../", ".."):
            if resolved[1:]:
                resolved.pop()
        elif segment not in ("./", "."):
            resolved.append(segment)

    return "".join(resolved).rstrip("/")


def attempt_to_decode_idna(string):
    try:
        return string.encode("utf8").decode("idna")
    except UnicodeError:
        return string


def decode_punycode_hostname(hostname, as_parts=False):
    parts = []

    for part in hostname.split("."):
        puny_header = part[:4].lower()

        if puny_header == "xn--":
            part = attempt_to_decode_idna(puny_header + part[4:])

        parts.append(part)

    if as_parts:
        return parts

    return ".".join(parts)


def fix_common_query_mistakes(query):
    return re.sub(MISTAKES_RE, "&", query)


def safe_parse_qs(query):
    return parse_qs(fix_common_query_mistakes(query))


def add_query_argument(url, name, value=None, quote=True):
    if quote:
        name = unshadowed_quote(name)

    if value == True or value is None:
        arg = name
    else:
        if quote:
            value = unshadowed_quote(str(value))

        arg = name + "=" + value

    query = None
    fragment = None

    s = url.rsplit("#", 1)

    if len(s) > 1:
        url, fragment = s

    s = url.rsplit("?", 1)

    if len(s) > 1:
        url, query = s

    if query:
        query += "&" + arg
    else:
        query = arg

    url += "?" + query

    if fragment is not None:
        url += "#" + fragment

    return url


def unsplit_netloc(username, password, hostname, port):
    if username and password:
        auth = username + ":" + password
    elif username:
        auth = username
    else:
        auth = None

    if auth:
        hostname = auth + "@" + hostname
    if port:
        hostname += ":" + str(port)

    return hostname


def safe_qsl_iter(query):
    for item in query.split("&"):
        if "=" not in item:
            yield item, None
        else:
            yield tuple(item.split("=", 1))


def safe_serialize_query_item(item):
    if item[1] is None:
        return item[0]

    return "%s=%s" % item


def safe_serialize_qsl(qsl):
    return "&".join(safe_serialize_query_item(item) for item in qsl)


def get_query_argument(url, key):
    o = safe_urlsplit(url)
    if not o.query:
        return None

    for q in safe_qsl_iter(o.query):
        if key == q[0]:
            if q[1] is None:
                return True
            return q[1]

    return None
