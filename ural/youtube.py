# =============================================================================
# Ural Youtube-related heuristic functions
# =============================================================================
#
# Collection of functions related to Youtube urls.
#
import re
from collections import namedtuple

from ural.utils import urlsplit, urlpathsplit, SplitResult
from ural.ensure_protocol import ensure_protocol
from ural.infer_redirection import infer_redirection
from ural.patterns import QUERY_VALUE_TEMPLATE, DOMAIN_TEMPLATE

YOUTUBE_DOMAINS_RE = re.compile(r'(?:youtube(?:\.googleapis)?\.[^.]+$|youtu\.be$)', re.I)
YOUTUBE_URL_RE = re.compile(DOMAIN_TEMPLATE % r'(?:[^.]+\.)*(?:youtube(?:\.googleapis)?\.[^.]+|youtu\.be)', re.I)
YOUTUBE_VIDEO_ID_RE = re.compile(r'^[a-zA-Z0-9_-]{11}$')
QUERY_V_RE = re.compile(QUERY_VALUE_TEMPLATE % r'v', re.I)
NEXT_V_RE = re.compile(r'next=%2Fwatch%3Fv%3D([^%&]+)', re.I)
NESTED_NEXT_V_RE = re.compile(r'next%3D%252Fwatch%253Fv%253D([^%&]+)', re.I)
FRAGMENT_V_RE = re.compile(r'^(?:%2F|/)watch(?:%3F|\?)v(?:%3D|=)([a-zA-Z0-9_-]{11})', re.I)

YOUTUBE_VIDEO_URL_TEMPLATE = 'https://www.youtube.com/watch?v=%s'
YOUTUBE_USER_URL_TEMPLATE = 'https://www.youtube.com/user/%s'
YOUTUBE_CHANNEL_ID_URL_TEMPLATE = 'https://www.youtube.com/channel/%s'
YOUTUBE_CHANNEL_NAME_URL_TEMPLAYE = 'https://www.youtube.com/c/%s'

YoutubeVideo = namedtuple('YoutubeVideo', ['id'])
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
        return bool(re.search(YOUTUBE_DOMAINS_RE, url.hostname))

    return bool(re.match(YOUTUBE_URL_RE, url))


def is_youtube_video_id(value):
    return bool(YOUTUBE_VIDEO_ID_RE.match(value))


def parse_youtube_url(url, fix_common_mistakes=True):
    """
    Function parsing the given url and returning either a YoutubeUser,
    YoutubeChannel, YoutubeVideo or None if nothing of information could be
    found.

    Args:
        url (str): Url to parse.
        fix_common_mistakes (bool, optional): Whether to fix common mistakes
            in Youtube urls as you can find them on the web. Defaults to `True`.

    """

    # Inferring redirection
    url = infer_redirection(url)

    # Continuation urls
    m = NEXT_V_RE.search(url) or NESTED_NEXT_V_RE.search(url)

    if m:
        return YoutubeVideo(id=m.group(1))

    # Parsing
    if isinstance(url, SplitResult):
        parsed = url
    else:
        url = ensure_protocol(url)
        parsed = urlsplit(url)

    if not is_youtube_url(parsed):
        return

    _, _, path, query, fragment = parsed

    # youtu.be
    if parsed.hostname.endswith('youtu.be'):

        if path.count('/') > 0:
            v = urlpathsplit(path)[0]

            if fix_common_mistakes:
                v = v[:11]

            if not is_youtube_video_id(v):
                return

            return YoutubeVideo(id=v)

        return

    # Hidden video in fragment
    if fragment:
        mv = FRAGMENT_V_RE.match(fragment)

        if mv:
            v = mv.group(1)

            if not is_youtube_video_id(v):
                return

            return YoutubeVideo(id=v)

    # Typical video url
    if path == '/watch':
        mv = QUERY_V_RE.search(query)

        if mv:
            v = mv.group(1)

            if fix_common_mistakes:
                v = v[:11]

            if not is_youtube_video_id(v):
                return

            return YoutubeVideo(id=v)

    # Video file
    elif (
        path.startswith('/v/') or
        path.startswith('/video/') or
        path.startswith('/embed/')
    ):
        v = urlpathsplit(path)[-1]

        if fix_common_mistakes:
            v = v[:11]

        if not is_youtube_video_id(v):
            return

        return YoutubeVideo(id=v)

    # Typical user url
    elif path.startswith('/user/'):
        user = urlpathsplit(path)[1]

        return YoutubeUser(id=None, name=user)

    # Channel path?
    elif path.startswith('/c/'):
        name = urlpathsplit(path)[1]

        return YoutubeChannel(id=None, name=name)

    elif path.startswith('/channel/'):
        cid = urlpathsplit(path)[1]

        return YoutubeChannel(id=cid, name=None)

    else:
        path = path.rstrip('/')
        if path.count('/') == 1:
            return YoutubeChannel(id=None, name=path.lstrip('/'))


def extract_video_id_from_youtube_url(url):
    parsed = parse_youtube_url(url)

    if parsed is None or not isinstance(parsed, YoutubeVideo):
        return

    return parsed.id


def normalize_youtube_url(url):
    parsed = parse_youtube_url(url)

    if parsed is None:

        # TODO: should we normalize at least www and protocol here?
        return url

    if isinstance(parsed, YoutubeVideo):
        return YOUTUBE_VIDEO_URL_TEMPLATE % parsed.id

    if isinstance(parsed, YoutubeUser):
        return YOUTUBE_USER_URL_TEMPLATE % parsed.name

    if isinstance(parsed, YoutubeChannel):
        if parsed.id is not None:
            return YOUTUBE_CHANNEL_ID_URL_TEMPLATE % parsed.id

        return YOUTUBE_CHANNEL_NAME_URL_TEMPLAYE % parsed.name

    raise TypeError('normalize_youtube_url: impossible path reached')
