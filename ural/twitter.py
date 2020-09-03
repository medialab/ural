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
USERNAME_EXCEPTIONS = ['home', 'hashtag', 'search', 'explore', 'settings', 'messages', 'notifications', 'explore', 'i']


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


def normalisation(username):
    """
    Small function used in extract_screen_name_from_twitter_url(url) in order to normalize username and deal
    with specific exceptions.
    Args:
        username (str) : username to test.

    Returns:
        username (str) or rise an exception.

    """
    if username in USERNAME_EXCEPTIONS:
        return None
    else:
        if username[0] == '@':
            username = username[1:]
        username = username.lower()
    return username


def extract_screen_name_from_twitter_url(url):
    """
    Function returning the screen_name

    Args:
        url (str) : Url from which we extract the screen_name if it exists

    Returns:
        str : screen_name if the url is a valid twitter url
              None otherwise

    """
    # Checking whether the url is a valid twitter url
    valid_url = is_twitter_url(url)
    url_fragmente = urlsplit(url)
    if valid_url and len(url_fragmente.path) >= 1:
        if len(url_fragmente.path) != 1:
            username = url_fragmente.path[1:].split('/')[0]
        else:
            username = url_fragmente.fragment[2:]
        return normalisation(username)
    else:
        return None
