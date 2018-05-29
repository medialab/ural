# =============================================================================
# Ural URL Normalization Function
# =============================================================================
#
# A handy function relying on heuristics to find and drop irrelevant or
# non-discriminant parts of a URL.
#
import re
from os.path import normpath, splitext
from urllib.parse import parse_qsl, urlparse, urlunparse

SCHEME_RE = re.compile('^[^:]*:?//')
IRRELEVANT_QUERY_RE = re.compile('^utm_(?:campaign|content|medium|source|term)|xtor$')
IRRELEVANT_SUBDOMAIN_RE = re.compile('\\b(?:www\\d?|mobile|m)\\.')


def stringify_qs(item):
    if item[1] == '':
        return item[0]

    return '%s=%s' % item


def normalize_url(url, drop_trailing_slash=True):
    """
    Function normalizing the given url by stripping it of usually
    non-discriminant parts such as irrelevant query items or sub-domains etc.

    This is a very useful utility when attempting to match similar urls
    written slightly differently when shared on social media etc.

    Args:
        url (str): Target URL as a string.
        drop_trailing_slash (bool, optional): Whether to drop trailing slash.
            Defaults to `True`.

    Returns:
        string: The normalized url.

    """

    # Ensuring scheme so parsing works correctly
    if not SCHEME_RE.match(url):
        url = 'http://' + url

    # Parsing
    scheme, netloc, path, params, query, fragment = urlparse(url)

    # Normalizing the path
    if path:
        path = normpath(path)

    # Dropping index:
    segments = path.split('/')

    if len(segments) != 0:
        last_segment = segments[-1]
        filename, ext = splitext(last_segment)

        if filename == 'index':
            segments.pop()
            path = '/'.join(segments)

    # Dropping irrelevant query items
    if query:
        qsl = parse_qsl(query, keep_blank_values=True)
        qsl = [stringify_qs(item) for item in qsl if not IRRELEVANT_QUERY_RE.match(item[0])]
        query = '&'.join(qsl)

    # Dropping fragment if it's not routing
    if fragment and len(fragment.split('/')) <= 1:
        fragment = ''

    # Dropping irrelevant subdomains
    netloc = re.sub(
        IRRELEVANT_SUBDOMAIN_RE,
        '',
        netloc
    )

    # Dropping scheme
    scheme = ''

    # Result
    result = (
        scheme,
        netloc,
        path,
        params,
        query,
        fragment
    )

    result = urlunparse(result)[2:]

    # Dropping trailing slash
    if drop_trailing_slash and result.endswith('/'):
        result = result.rstrip('/')

    return result
