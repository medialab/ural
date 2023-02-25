# =============================================================================
# Ural Twitter-related heuristic functions
# =============================================================================
#
# Collection of functions related to Twitter urls.
#
import re
from collections import namedtuple

from ural.patterns import DOMAIN_TEMPLATE
from ural.utils import SplitResult, safe_urlsplit, urlpathsplit

TWITTER_DOMAINS_RE = re.compile(r"twitter\.com", re.I)
TWITTER_URL_RE = re.compile(DOMAIN_TEMPLATE % r"(?:[^.]+\.)*twitter\.com", re.I)
TWITTER_FRAGMENT_ROUTING_RE = re.compile(r"^!/?")
TWITTER_SCREEN_NAME_BLACKLIST = {
    "explore",
    "home",
    "hashtag",
    "i",
    "messages",
    "notifications",
    "search",
    "settings",
}

TwitterTweet = namedtuple("TwitterTweet", ["user_screen_name", "id"])
TwitterUser = namedtuple("TwitterUser", ["screen_name"])
TwitterList = namedtuple("TwitterList", ["id"])


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

    if username.startswith("@"):
        username = username[1:]

    return username.lower()


def parse_twitter_url(url):
    """
    Function returning a parsed result from a given Twitter url.

    Args:
        url (str) : Url from which to extract information if found.

    Returns:
        TwitterTweet (namedtuple containing a user_screen_name and a tweet id) instance if the url is a link to a tweet
        or TwitterUser (namedtuple containing a user_screen_name) instance if the url is a link to a twitter user,
        or TwitterList (namedtuple containing a list id) instance if the url is a link to a twitter list,
        None othewise.

    """

    if not is_twitter_url(url):
        return None

    parsed = safe_urlsplit(url)
    path = urlpathsplit(parsed.path)

    if path:
        user_screen_name = normalize_screen_name(path[0])

        if user_screen_name is None:
            if path[0] == "i" and path[1] == "lists" and len(path) == 3:
                return TwitterList(id=path[2])
            return None

        if len(path) == 3:
            return TwitterTweet(user_screen_name=user_screen_name, id=path[2])

        return TwitterUser(screen_name=user_screen_name)

    if parsed.fragment.startswith("!"):
        path = re.sub(TWITTER_FRAGMENT_ROUTING_RE, "", parsed.fragment)

        return parse_twitter_url("twitter.com/" + path)

    return None


def extract_screen_name_from_twitter_url(url):
    """
    Function returning the screen_name from a given Twitter url.

    Args:
        url (str) : Url from which we extract the screen_name if found.

    Returns:
        str : screen_name if the url is a valid twitter url, None otherwise.

    """

    parsed_twitter_url = parse_twitter_url(url)

    if isinstance(parsed_twitter_url, TwitterUser):
        return parsed_twitter_url.screen_name

    if isinstance(parsed_twitter_url, TwitterTweet):
        return parsed_twitter_url.user_screen_name

    return None
