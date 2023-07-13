# -*- coding: utf-8 -*-
# =============================================================================
# Ural Could Be RSS URL
# =============================================================================
#
# Function returning whether the given url should be a rss feed url.
#
import re

from ural.utils import safe_urlsplit
from ural.get_hostname import get_hostname

HOSTNAME_RULES = [
    ("linkedin.com", "", False),
    ("news.google.com", "__i/rss", False),
    ("feeds.feedburner.com", "", True),
    ("feeds2.feedburner.com", "", True),
    ("news.google.com", "rss/topics", True),
]

QUERY_RE = re.compile(
    r"((page\=backend)|(?:feed|format|type)\=(?:xml|feed|atom|rss))", re.I
)
OBVIOUS_EXT_RE = re.compile(
    r"((^$)|(\/[^\.]*$)|(.+\.(?:xml|php|json|atom|rss)$))", re.I
)
FILE_RE = re.compile(
    r"(((?:feeds?|rss|atoms?|blogs?)\.(?:xml|atom|rss|php|json)$)|((?:news|latest|index|posts?)\.(?:xml|atom|rss)$)|(.+\.(?:rss|atom)$)|((?:[\/\.\-_]|^)(?:rss|feeds?|atom)[0-9]{,10}(?:[\/\.\-_]|$)))",
    re.I,
)


def could_be_rss(url):
    split = safe_urlsplit(url)
    hostname = get_hostname(url)

    if not hostname:
        return False

    for h, p, r in HOSTNAME_RULES:
        if hostname == h:
            if p in split.path:
                return r

            break

    if split.query and QUERY_RE.search(split.query):
        return True

    if split.path and not OBVIOUS_EXT_RE.match(split.path):
        return False

    if split.path and FILE_RE.search(split.path):
        return True

    return False
