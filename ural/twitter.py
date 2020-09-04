# =============================================================================
# Ural Twitter-related heuristic functions
# =============================================================================
#
# Collection of functions related to Twitter urls.
#
import re

from ural.patterns import DOMAIN_TEMPLATE
from ural.utils import SplitResult, safe_urlsplit, urlpathsplit

TWITTER_DOMAINS_RE = re.compile(r'twitter\.com', re.I)
TWITTER_URL_RE = re.compile(DOMAIN_TEMPLATE % r'(?:[^.]+\.)*twitter\.com', re.I)
TWITTER_FRAGMENT_ROUTING_RE = re.compile(r'^!/?')
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

    parsed = safe_urlsplit(url)
    path = urlpathsplit(parsed.path)

    if path:
        return normalize_screen_name(path[0])

    if parsed.fragment.startswith('!'):
        path = re.sub(TWITTER_FRAGMENT_ROUTING_RE, '', parsed.fragment)

        return normalize_screen_name(path)

    return None
