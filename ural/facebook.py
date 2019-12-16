# =============================================================================
# Ural Facebook-related heuristic functions
# =============================================================================
#
# Collection of functions crafted to work with Facebook's urls.
#
import re

from ural.ensure_protocol import ensure_protocol
from ural.patterns import DOMAIN_TEMPLATE, QUERY_VALUE_IN_URL_TEMPLATE

from ural.utils import (
    parse_qs,
    unquote,
    urljoin,
    urlpathsplit,
    urlsplit,
    urlunsplit,
    safe_urlsplit,
    SplitResult
)

BASE_FACEBOOK_URL = 'https://www.facebook.com'

FACEBOOK_DOMAIN_RE = re.compile(r'(?:facebook\.[^.]+$|fb\.me$)', re.I)
FACEBOOK_URL_RE = re.compile(DOMAIN_TEMPLATE % r'(?:[^.]+\.)*(?:facebook\.[^.]+|fb\.me)', re.I)
MOBILE_REPLACE_RE = re.compile(r'^([^.]+\.)?facebook\.', re.I)

URL_EXTRACT_RE = re.compile(QUERY_VALUE_IN_URL_TEMPLATE % r'u')


def is_facebook_url(url):
    """
    Function returning whether the given url is a valid Facebook url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Facebook.

    """
    if isinstance(url, SplitResult):
        return bool(re.search(FACEBOOK_DOMAIN_RE, url.hostname))

    return bool(re.match(FACEBOOK_URL_RE, url))


def is_facebook_link(url):
    splitted = safe_urlsplit(url)

    if not splitted.hostname or '.facebook.' not in splitted.hostname:
        return False

    if splitted.path != '/l.php':
        return False

    return True


def extract_url_from_facebook_link(url):
    m = URL_EXTRACT_RE.search(url)

    if m is None:
        return None

    return unquote(m.group(1))


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


class FacebookParsedItem(object):
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        for attr in self.__slots__:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True


class FacebookUser(FacebookParsedItem):
    __slots__ = ('id', 'handle')

    def __init__(self, user_id, handle=None):
        self.id = user_id
        self.handle = handle

    @property
    def url(self):
        if self.handle is None:
            return urljoin(BASE_FACEBOOK_URL, '/profile.php?id=%s' % self.id)

        return urljoin(BASE_FACEBOOK_URL, '/%s' % self.handle)

    def __repr__(self):
        class_name = self.__class__.__name__

        return (
            '<%(class_name)s id=%(id)s handle=%(handle)s>'
        ) % {
            'class_name': class_name,
            'id': self.id,
            'handle': self.handle
        }


class FacebookHandle(FacebookParsedItem):
    __slots__ = ('handle',)

    def __init__(self, handle):
        self.handle = handle

    @property
    def url(self):
        return urljoin(BASE_FACEBOOK_URL, '/profile.php?id=%s' % self.id)

    def __repr__(self):
        class_name = self.__class__.__name__

        return (
            '<%(class_name)s handle=%(handle)s>'
        ) % {
            'class_name': class_name,
            'handle': self.handle
        }


def parse_facebook_url(url, allow_relative_urls=False):

    # Allowing relative urls scraped from facebook?
    if (
        allow_relative_urls and
        not url.startswith('http://') and
        not url.startswith('https://') and
        'facebook.' not in url
    ):
        url = urljoin(BASE_FACEBOOK_URL, url)
    else:
        if not is_facebook_url(url):
            return None

    splitted = safe_urlsplit(url)

    if not splitted.path or splitted.path == '/':
        return None

    # Profile path
    if splitted.path == '/profile.php':
        query = parse_qs(splitted.query)
        user_id = query['id'][0]
        return FacebookUser(user_id)

    # People path
    if splitted.path.startswith('/people'):
        parts = urlpathsplit(splitted.path)
        user_id = parts[2]
        return FacebookUser(user_id)

    # Handle path
    if splitted.path:
        parts = urlpathsplit(splitted.path)

        if not parts[0].endswith('.php'):
            return FacebookHandle(parts[0])

    return None
