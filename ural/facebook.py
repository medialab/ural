# =============================================================================
# Ural Facebook-related heuristic functions
# =============================================================================
#
# Collection of functions crafted to work with Facebook's urls.
#
import re
from collections import namedtuple
try:
    from urllib.parse import parse_qs, urljoin, urlsplit, urlunsplit
except ImportError:
    from urlparse import parse_qs, urljoin, urlsplit, urlunsplit

from ural.ensure_protocol import ensure_protocol

BASE_FACEBOOK_URL = 'https://www.facebook.com'

MOBILE_REPLACE_RE = re.compile(r'^([^.]+\.)?facebook\.', re.I)


def convert_facebook_url_to_mobile(url):
    """
    Function parsing the given facebook url and returning the same but for
    the mobile website.
    """
    safe_url = ensure_protocol(url)

    has_protocol = safe_url == url

    scheme, netloc, path, query, fragment = urlsplit(safe_url)

    if 'facebook' not in netloc:
        raise Exception('ural.facebook.convert_facebook_url_to_mobile: %s is not a facebook url' % url)

    netloc = re.sub(MOBILE_REPLACE_RE, 'm.facebook.', netloc)

    result = (
        scheme,
        netloc,
        path,
        query,
        fragment
    )

    result = urlunsplit(result)

    if not has_protocol:
        result = result.split('://', 1)[-1]

    return result


FacebookUser = namedtuple('FacebookUser', ['id', 'handle', 'url'])


def extract_user_from_facebook_url(url):
    if 'facebook.' not in url:
        url = urljoin(BASE_FACEBOOK_URL, url)

    url = ensure_protocol(url)

    parsed = urlsplit(url)

    if parsed.path == '/profile.php':
        query = parse_qs(parsed.query)

        user_id = query['id'][0]
        user_handle = None
        user_url = urljoin(BASE_FACEBOOK_URL, '/profile.php?id=%s' % user_id)
    elif parsed.path.startswith('/people'):
        parts = parsed.path.split('/')

        user_id = parts[3]
        user_handle = None
        user_url = urljoin(BASE_FACEBOOK_URL, '/profile.php?id=%s' % user_id)
    else:
        user_id = None
        user_handle = parsed.path.split('/')[1]
        user_url = urljoin(BASE_FACEBOOK_URL, '/%s' % user_handle)

    return FacebookUser(
        user_id,
        user_handle,
        user_url
    )
