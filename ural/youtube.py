# =============================================================================
# Ural Youtube-related heuristic functions
# =============================================================================
#
# Collection of functions related to Youtube urls.
#
import re
from collections import namedtuple
try:
    from urllib.parse import urlsplit, parse_qs, SplitResult
except ImportError:
    from urlparse import urlsplit, parse_qs, SplitResult

from ural.ensure_protocol import ensure_protocol
from ural.patterns import QUERY_VALUE

YOUTUBE_DOMAIN_RE = re.compile(r'(?:youtube(?:\.googleapis)?\.[^.]+$|youtu\.be$)', re.I)
QUERY_V_RE = re.compile(QUERY_VALUE % r'v', re.I)

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
    if isinstance(url, SplitResult):
        parsed = url
    else:
        url = ensure_protocol(url)
        parsed = urlsplit(url)

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

    # Channel path?
    elif path.startswith('/c/'):
        name = path.split('/')[2]

        return YoutubeChannel(id=None, name=name)

    elif path.startswith('/channel/'):
        cid = path.split('/')[2]

        return YoutubeChannel(id=cid, name=None)

    else:
        if path.count('/') == 1:
            return YoutubeChannel(id=None, name=path.lstrip('/'))


# TODO: normalizers, basic extractors
