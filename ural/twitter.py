# =============================================================================
# Ural Twitter-related heuristic functions
# =============================================================================
#
# Collection of functions related to Twitter urls.
#
import re

from ural.patterns import DOMAIN_TEMPLATE
from ural.utils import SplitResult, urlsplit, urlpathsplit

TWITTER_DOMAINS_RE = re.compile(r'twitter\.com', re.I)
TWITTER_URL_RE = re.compile(DOMAIN_TEMPLATE % r'(?:[^.]+\.)*twitter\.com', re.I)
TWITTER_SCREEN_NAME_BLACKLIST = {
    'explore',
    'home',
    'hashtag',
    'i',
    'messages',
    'notifications',
    'search',
    'settings'
}


def is_twitter_url(url):
    """
    Function returning whether the given url is a valid Twitter url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Youtube.

    """
    if isinstance(url, SplitResult):
        return bool(re.search(TWITTER_DOMAINS_RE, url.hostname))

    return bool(re.match(TWITTER_URL_RE, url))


def normalize_screen_name(username):
    if username in TWITTER_SCREEN_NAME_BLACKLIST:
        return None

    if username.startswith('@'):
        username = username[1:]

    return username.lower()


def extract_screen_name_from_twitter_url(url):
    """
    Function returning the screen_name from a given Twitter url.

    Args:
        url (str) : Url from which we extract the screen_name if found.

    Returns:
        str : screen_name if the url is a valid twitter url, None otherwise.

    """

    # Checking whether the url is a valid twitter url
    if not is_twitter_url(url):
        return None

    parsed = urlsplit(url)
    path = urlpathsplit(parsed.path)

    if len(path) >= 1:
        if len(path[0]) >= 1:
            username = path[0]
            return normalize_screen_name(username)
    elif len(path) == 0:
        username = urlpathsplit(parsed.fragment)[1]
        return normalize_screen_name(username)
    return None
