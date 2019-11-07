# =============================================================================
# Ural Youtube-related heuristic functions
# =============================================================================
#
# Collection of functions related to Youtube urls.
#
import re
from collections import namedtuple
try:
    from urllib.parse import urlsplit, SplitResult
except ImportError:
    from urlparse import urlsplit, SplitResult

from ural.ensure_protocol import ensure_protocol
from ural.patterns import QUERY_VALUE

YOUTUBE_DOMAIN_RE = re.compile(r'(?:youtube(?:\.googleapis)?\.[^.]+$|youtu\.be$)', re.I)
QUERY_V_RE = re.compile(QUERY_VALUE % r'v', re.I)
NEXT_V_RE = re.compile(r'next=%2Fwatch%3Fv%3D([^%&]+)', re.I)
NESTED_NEXT_V_RE = re.compile(r'next%3D%252Fwatch%253Fv%253D([^%&]+)', re.I)

YoutubeVideo = namedtuple('YoutubeVideo', ['id', 'user'])
YoutubeUser = namedtuple('YoutubeUser', ['id', 'name'])
YoutubeChannel = namedtuple('YoutubeChannel', ['id', 'name'])


def is_youtube_url(url):
    """
    Function returning whether the given url is a valid Youtube url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Youtube.

    """

    if isinstance(url, SplitResult):
        parsed = url
    else:
        url = ensure_protocol(url)
        parsed = urlsplit(url)

    return bool(re.search(YOUTUBE_DOMAIN_RE, parsed.hostname))


def parse_youtube_url(url):

    # Continuation urls
    m = NEXT_V_RE.search(url) or NESTED_NEXT_V_RE.search(url)

    if m:
        return YoutubeVideo(id=m.group(1), user=None)

    # Parsing
    if isinstance(url, SplitResult):
        parsed = url
    else:
        url = ensure_protocol(url)
        parsed = urlsplit(url)

    if not is_youtube_url(parsed):
        return

    _, _, path, query, _ = parsed

    # Typical video url
    if path == '/watch':
        mv = QUERY_V_RE.search(query)

        if mv:
            return YoutubeVideo(id=mv.group(1), user=None)

    # Video file
    elif (
        path.startswith('/v/') or
        path.startswith('/video/') or
        path.startswith('/embed/')
    ):
        v = path.rsplit('/', 1)[-1]

        return YoutubeVideo(id=v, user=None)

    # Typical user url
    elif path.startswith('/user/'):
        user = path.split('/')[2]

        return YoutubeUser(id=None, name=user)

    elif path.startswith('/profile_redirector/'):
        uid = path.split('/')[2]

        return YoutubeUser(id=uid, name=None)

    # Channel path?
    elif path.startswith('/c/'):
        name = path.split('/')[2]

        return YoutubeChannel(id=None, name=name)

    elif path.startswith('/channel/'):
        cid = path.split('/')[2]

        return YoutubeChannel(id=cid, name=None)

    else:
        path = path.rstrip('/')
        if path.count('/') == 1:
            return YoutubeChannel(id=None, name=path.lstrip('/'))


# TODO: normalizers, basic extractors
