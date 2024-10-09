import re

from ural.patterns import DOMAIN_TEMPLATE
from ural.utils import SplitResult
from ural import get_domain_name, urlpathsplit


REDDIT_DOMAIN_RE = re.compile(r"(?:reddit\.[^.]+$|redd\.it$)", re.I)
REDDIT_URL_RE = re.compile(DOMAIN_TEMPLATE % r"(?:[^.]+\.)*(?:reddit\.[^.]+|redd\.it)", re.I)


def is_reddit_url(url):
    if isinstance(url, SplitResult):
        return bool(re.search(REDDIT_DOMAIN_RE, url.hostname))

    return bool(re.match(REDDIT_URL_RE, url))


def is_subreddit_url(url):
    if not is_reddit_url(url):
        return False
    
    return (
        '/r/' in url
    )


def is_reddit_user_url(url):
    if not is_reddit_url(url):
        return False
    
    return (
        '/user/' in url
    )


def is_reddit_post_url(url):
    if not is_reddit_url(url):
        return False
    
    return (
        '/r/' in url and '/comments/' in url
    )


def convert_reddit_url_to_old_url(url):
    domain = get_domain_name(url)
    path = urlpathsplit(url)
    return f"https://old.{domain}/" + "/".join(path) + "/"


def convert_old_reddit_url_to_new_url(url):
    domain = get_domain_name(url)
    path = urlpathsplit(url)
    return f"https://www.{domain}/" + "/".join(path) + "/"


