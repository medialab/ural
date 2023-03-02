# =============================================================================
# Ural Instagram-related heuristic functions
# =============================================================================
#
# Collection of functions related to Instagram urls.
#
import re
from collections import namedtuple

from ural.utils import urlpathsplit, safe_urlsplit, SplitResult
from ural.patterns import DOMAIN_TEMPLATE

INSTAGRAM_POST_SHORTCODE_RE = re.compile(r"^[a-zA-Z0-9_\-]+$")
INSTAGRAM_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_\-\.]+$")
INSTAGRAM_DOMAIN_RE = re.compile(r"instagram.com$", re.I)
INSTAGRAM_URL_RE = re.compile(DOMAIN_TEMPLATE % r"(?:[^.]+\.)*instagram.com", re.I)
INSTAGRAM_NOT_A_USER_SET = {
    "accounts",
    "ads",
    "direct",
    "directory",
    "emails",
    "explore",
    "push",
    "reels",
    "session",
    "settings",
    "stories",
    "web",
    "your_activity"
}

InstagramUser = namedtuple("InstagramUser", ["name"])
InstagramPost = namedtuple("InstagramPost", ["id", "name"])
InstagramReel = namedtuple("InstagramReel", ["id"])


def is_instagram_post_shortcode(value):
    return bool(re.search(INSTAGRAM_POST_SHORTCODE_RE, value))


def is_instagram_username(value):
    return bool(re.search(INSTAGRAM_USERNAME_RE, value)) and value not in INSTAGRAM_NOT_A_USER_SET


def is_instagram_url(url):
    """
    Function returning whether the given url is a valid Instagram url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Instagram.

    """
    if isinstance(url, SplitResult):
        return bool(re.search(INSTAGRAM_DOMAIN_RE, url.hostname))

    return bool(re.match(INSTAGRAM_URL_RE, url))


def parse_instagram_url(url):
    """
    Function parsing the given url and returning either a InstagramPost,
    InstagramUser or None if nothing of information could be found.

    Args:
        url (str): Url to parse.

    """
    if not is_instagram_url(url):
        return None

    parsed = safe_urlsplit(url)
    path = urlpathsplit(parsed.path)

    if not path:
        return None

    if path[0] == "p" and len(path) >= 2:

        if is_instagram_post_shortcode(path[1]):
            return InstagramPost(id=path[1], name=None)

        return None

    elif path[0] == "reel" and len(path) >= 2:

        if is_instagram_post_shortcode(path[1]):
            return InstagramReel(id=path[1])

        return None

    elif path[0] == "reels" and len(path) >= 2:

        if (
            is_instagram_post_shortcode(path[1])
            and path[1] != "videos"
        ):
            return InstagramReel(id=path[1])

        elif (
            len(path) >= 3
            and path[1] == "videos"
            and is_instagram_post_shortcode(path[2])
            and path[2] != "videos"
        ):
            return InstagramReel(id=path[2])

        return None

    elif is_instagram_username(path[0]):

        if (
            len(path) >= 3
            and path[1] == "p"
            and is_instagram_post_shortcode(path[2])
        ):
            return InstagramPost(id=path[2], name=path[0])

        return InstagramUser(name=path[0])

    return None


def extract_username_from_instagram_url(url):
    parsed = parse_instagram_url(url)

    if not isinstance(parsed, (InstagramPost, InstagramUser)):
        return

    return parsed.name
