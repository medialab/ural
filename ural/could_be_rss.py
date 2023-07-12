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

HOSTNAMES_BAD = ["linkedin.com", "news.google.com"]
HOSTNAMES_GOOD = ["feeds.feedburner.com", "feeds2.feedburner.com"]
QUERY_RE = re.compile(r"(?:feed|format|type)\=(?:xml|feed|atom|rss)", re.I)
FILE_RE = re.compile(
    r"(((?:feeds?|rss|atoms?|blogs?)\.(?:xml|atom|rss|php|json)$)|((?:news|latest|index|posts?)\.(?:xml|atom|rss)$)|(.+\.(?:rss|atom)$)|((?:[\/\.\-_]|^)(?:rss|feeds?|atom)[0-9]{,10}(?:[\/\.\-_]|$)))",
    re.I,
)


def could_be_rss(url):
    split = safe_urlsplit(url)
    hostname = get_hostname(url)

    if not hostname or hostname in HOSTNAMES_BAD:
        return False
    if hostname in HOSTNAMES_GOOD:
        return True
    if split.query and QUERY_RE.search(split.query):
        return True
    if split.path and FILE_RE.search(split.path):
        return True
    return False
