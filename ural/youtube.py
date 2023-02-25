# =============================================================================
# Ural Youtube-related heuristic functions
# =============================================================================
#
# Collection of functions related to Youtube urls.
#
import re
from collections import namedtuple

from ural.classes.hostname_trie_set import HostnameTrieSet
from ural.utils import urlpathsplit, safe_urlsplit
from ural.infer_redirection import infer_redirection
from ural.patterns import QUERY_VALUE_TEMPLATE

YOUTUBE_DOMAINS = [
    "blog.youtube",
    "rewind.youtube",
    "youtu.be",
    "youtube.ae",
    "youtube.al",
    "youtube.am",
    "youtube.at",
    "youtube.az",
    "youtube.ba",
    "youtube.be",
    "youtube.bg",
    "youtube.bh",
    "youtube.bo",
    "youtube.by",
    "youtube.ca",
    "youtube.cat",
    "youtube.ch",
    "youtube.cl",
    "youtube.co",
    "youtube.co.ae",
    "youtube.co.at",
    "youtube.co.cr",
    "youtube.co.hu",
    "youtube.co.id",
    "youtube.co.il",
    "youtube.co.in",
    "youtube.co.jp",
    "youtube.co.ke",
    "youtube.co.kr",
    "youtube.co.ma",
    "youtube.co.nz",
    "youtube.co.th",
    "youtube.co.tz",
    "youtube.co.ug",
    "youtube.co.uk",
    "youtube.co.ve",
    "youtube.co.za",
    "youtube.co.zw",
    "youtube.com",
    "youtube.com.ar",
    "youtube.com.au",
    "youtube.com.az",
    "youtube.com.bd",
    "youtube.com.bh",
    "youtube.com.bo",
    "youtube.com.br",
    "youtube.com.by",
    "youtube.com.co",
    "youtube.com.do",
    "youtube.com.ec",
    "youtube.com.ee",
    "youtube.com.eg",
    "youtube.com.es",
    "youtube.com.gh",
    "youtube.com.gr",
    "youtube.com.gt",
    "youtube.com.hk",
    "youtube.com.hn",
    "youtube.com.hr",
    "youtube.com.jm",
    "youtube.com.jo",
    "youtube.com.kw",
    "youtube.com.lb",
    "youtube.com.lv",
    "youtube.com.ly",
    "youtube.com.mk",
    "youtube.com.mt",
    "youtube.com.mx",
    "youtube.com.my",
    "youtube.com.ng",
    "youtube.com.ni",
    "youtube.com.om",
    "youtube.com.pa",
    "youtube.com.pe",
    "youtube.com.ph",
    "youtube.com.pk",
    "youtube.com.pt",
    "youtube.com.py",
    "youtube.com.qa",
    "youtube.com.ro",
    "youtube.com.sa",
    "youtube.com.sg",
    "youtube.com.sv",
    "youtube.com.tn",
    "youtube.com.tr",
    "youtube.com.tw",
    "youtube.com.ua",
    "youtube.com.uy",
    "youtube.com.ve",
    "youtube.cr",
    "youtube.cz",
    "youtube.de",
    "youtube.dk",
    "youtube.ee",
    "youtube.es",
    "youtube.fi",
    "youtube.fr",
    "youtube.ge",
    "youtube.googleapis.com",
    "youtube.gr",
    "youtube.gt",
    "youtube.hk",
    "youtube.hr",
    "youtube.hu",
    "youtube.ie",
    "youtube.in",
    "youtube.iq",
    "youtube.is",
    "youtube.it",
    "youtube.jo",
    "youtube.jp",
    "youtube.kr",
    "youtube.kz",
    "youtube.la",
    "youtube.lk",
    "youtube.lt",
    "youtube.lu",
    "youtube.lv",
    "youtube.ly",
    "youtube.ma",
    "youtube.md",
    "youtube.me",
    "youtube.mk",
    "youtube.mn",
    "youtube.mx",
    "youtube.my",
    "youtube.ng",
    "youtube.ni",
    "youtube.nl",
    "youtube.no",
    "youtube.pa",
    "youtube.pe",
    "youtube.ph",
    "youtube.pk",
    "youtube.pl",
    "youtube.pr",
    "youtube.pt",
    "youtube.qa",
    "youtube.ro",
    "youtube.rs",
    "youtube.ru",
    "youtube.sa",
    "youtube.se",
    "youtube.sg",
    "youtube.si",
    "youtube.sk",
    "youtube.sn",
    "youtube.soy",
    "youtube.sv",
    "youtube.tn",
    "youtube.tv",
    "youtube.ua",
    "youtube.ug",
    "youtube.uy",
    "youtube.vn",
    "youtubeeducation.com",
    "youtubekids.com",
    "yt.be",
]
YOUTUBE_VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
QUERY_V_RE = re.compile(QUERY_VALUE_TEMPLATE % r"v", re.I)
NEXT_V_RE = re.compile(r"next=%2Fwatch%3Fv%3D([^%&]+)", re.I)
NESTED_NEXT_V_RE = re.compile(r"next%3D%252Fwatch%253Fv%253D([^%&]+)", re.I)
FRAGMENT_V_RE = re.compile(
    r"^(?:%2F|/)watch(?:%3F|\?)v(?:%3D|=)([a-zA-Z0-9_-]{11})", re.I
)

YOUTUBE_VIDEO_URL_TEMPLATE = "https://www.youtube.com/watch?v=%s"
YOUTUBE_USER_URL_TEMPLATE = "https://www.youtube.com/user/%s"
YOUTUBE_CHANNEL_ID_URL_TEMPLATE = "https://www.youtube.com/channel/%s"

# NOTE: it's possible this does not work with all channels...
# Sometimes I think you need 'https://www.youtube.com/%s' instead
# but there is no way to infer this...
YOUTUBE_CHANNEL_NAME_URL_TEMPLAYE = "https://www.youtube.com/c/%s"

YOUTUBE_CHANNEL_NAME_BLACKLIST = {
    "about",
    "account",
    "ads",
    "creators",
    "feed",
    "howyoutubeworks",
    "new",
    "paid_memberships",
    "playlist",
    "reporthistory",
    "results",
    "t",
}

YoutubeVideo = namedtuple("YoutubeVideo", ["id"])
YoutubeUser = namedtuple("YoutubeUser", ["id", "name"])
YoutubeChannel = namedtuple("YoutubeChannel", ["id", "name"])


# NOTE: we use a trie to perform efficient queries and so we don't
# need to test every domain/subdomain linearly
YOUTUBE_DOMAINS_TRIE = HostnameTrieSet()

for domain in YOUTUBE_DOMAINS:
    YOUTUBE_DOMAINS_TRIE.add(domain)


def is_youtube_url(url):
    """
    Function returning whether the given url is a valid Youtube url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Youtube.

    """
    return YOUTUBE_DOMAINS_TRIE.match(url)


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
    parsed = safe_urlsplit(url)

    if not is_youtube_url(parsed):
        return

    _, _, path, query, fragment = parsed

    # youtu.be
    if parsed.hostname.endswith("youtu.be"):

        if path.count("/") > 0:
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
    if path == "/watch":
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
        path.startswith("/v/")
        or path.startswith("/video/")
        or path.startswith("/embed/")
    ):
        v = urlpathsplit(path)[-1]

        if fix_common_mistakes:
            v = v[:11]

        if not is_youtube_video_id(v):
            return

        return YoutubeVideo(id=v)

    # Typical user url
    elif path.startswith("/user/"):
        splitted_path = urlpathsplit(path)

        if len(splitted_path) < 2:
            return None

        user = splitted_path[1]

        return YoutubeUser(id=None, name=user)

    # Channel path?
    elif path.startswith("/c/"):
        # NOTE: there is an edge case here with the "c" channel that does exist
        # which means /c will parse as a channel, but /c/ will not but I don't
        # want to spend too much time on this weirdness.

        splitted_path = urlpathsplit(path)

        if len(splitted_path) < 2:
            return None

        name = splitted_path[1]

        return YoutubeChannel(id=None, name=name)

    elif path.startswith("/channel/"):
        splitted_path = urlpathsplit(path)

        if len(splitted_path) < 2:
            return None

        cid = splitted_path[1]

        return YoutubeChannel(id=cid, name=None)

    else:
        path = path.rstrip("/")
        if path.count("/") == 1:
            name = path.lstrip("/")

            if name in YOUTUBE_CHANNEL_NAME_BLACKLIST:
                return

            return YoutubeChannel(id=None, name=name)


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

    raise TypeError("normalize_youtube_url: impossible path reached")
