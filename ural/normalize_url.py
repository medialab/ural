# =============================================================================
# Ural URL Normalization Function
# =============================================================================
#
# A handy function relying on heuristics to find and drop irrelevant or
# non-discriminant parts of a URL.
#
import re
from os.path import normpath, splitext
try:
    from urllib.parse import parse_qsl, urlsplit, urlunsplit
except ImportError:
    from urlparse import parse_qsl, urlsplit, urlunsplit

from ural.patterns import PROTOCOL_RE

IRRELEVANT_QUERY_RE = re.compile(
    r'^(?:__twitter_impression|echobox|fbclid|utm_.+|amp_.+|amp|s?een|xt(?:loc|ref|cr|np|or|s))$', re.I)

IRRELEVANT_SUBDOMAIN_RE = re.compile(r'\b(?:www\d?|mobile|m)\.', re.I)

IRRELEVANT_QUERY_COMBOS = {
    'ref': ('fb', 'tw', 'tw_i'),
    'platform': ('hootsuite')
}


def attempt_to_decode_idna(string):
    try:
        return string.encode('utf8').decode('idna')
    except:
        return string


def stringify_qs(item):
    if item[1] == '':
        return item[0]

    return '%s=%s' % item


def should_strip_query_item(item):
    key = item[0].lower()

    if IRRELEVANT_QUERY_RE.match(key):
        return True

    value = item[1]

    if key in IRRELEVANT_QUERY_COMBOS:
        return value in IRRELEVANT_QUERY_COMBOS[key]

    return False


def normalize_url(url, parsed=False, sort_query=True, strip_authentication=True,
                  strip_trailing_slash=False, strip_index=True, strip_protocol=True, strip_irrelevant_subdomain=True):
    """
    Function normalizing the given url by stripping it of usually
    non-discriminant parts such as irrelevant query items or sub-domains etc.

    This is a very useful utility when attempting to match similar urls
    written slightly differently when shared on social media etc.

    Args:
        url (str): Target URL as a string.
        sort_query (bool, optional): Whether to sort query items or not.
            Defaults to `True`.
        strip_authentication (bool, optional): Whether to drop authentication.
            Defaults to `True`.
        strip_trailing_slash (bool, optional): Whether to drop trailing slash.
            Defaults to `False`.
        strip_index (bool, optional): Whether to drop trailing index at the end
            of the url. Defaults to `True`.

    Returns:
        string: The normalized url.

    """

    has_protocol = PROTOCOL_RE.match(url)
    # Ensuring scheme so parsing works correctly
    if not has_protocol:
        url = 'http://' + url

    # Parsing
    scheme, netloc, path, query, fragment = urlsplit(url)

    # Handling punycode
    if 'xn--' in netloc:
        netloc = '.'.join(
            attempt_to_decode_idna(x) for x in netloc.split('.')
        )

    # Dropping :80 & :443
    if netloc.endswith(':80'):
        netloc = netloc[:-3]
    elif netloc.endswith(':443'):
        netloc = netloc[:-4]

    # Normalizing the path
    if path:
        trailing_slash = False
        if path.endswith('/') and len(path) > 1:
            trailing_slash = True
        path = normpath(path)
        if trailing_slash and not strip_trailing_slash:
            path = path + '/'

    # Dropping index:
    if strip_index:
        segments = path.rsplit('/', 1)

        if len(segments) != 0:
            last_segment = segments[-1]
            filename, ext = splitext(last_segment)

            if filename == 'index':
                segments.pop()
                path = '/'.join(segments)

    # Dropping irrelevant query items
    if query:
        qsl = parse_qsl(query, keep_blank_values=True)
        qsl = [
            stringify_qs(item)
            for item in qsl
            if not should_strip_query_item(item)
        ]

        if sort_query:
            qsl = sorted(qsl)

        query = '&'.join(qsl)

    # Dropping fragment if it's not routing
    if fragment and len(fragment.split('/')) <= 1:
        fragment = ''

    # Dropping irrelevant subdomains
    if strip_irrelevant_subdomain:
        netloc = re.sub(
            IRRELEVANT_SUBDOMAIN_RE,
            '',
            netloc
        )

    # Dropping scheme
    if strip_protocol or not has_protocol:
        scheme = ''

    # Dropping authentication
    if strip_authentication:
        netloc = netloc.split('@', 1)[-1]

    # Result
    result = (
        scheme,
        netloc.lower(),
        path,
        query,
        fragment
    )
    if parsed:
        return result

    if strip_protocol or not has_protocol:
        result = urlunsplit(result)[2:]
    else:
        result = urlunsplit(result)

    # Dropping trailing slash
    if strip_trailing_slash and result.endswith('/'):
        result = result.rstrip('/')

    return result
