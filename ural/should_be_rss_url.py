# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Be RSS URL
# =============================================================================
#
# Function returning whether the given url should be a rss feed url.
#
import re

from ural.utils import urlpathsplit
from ural.utils import urlsplit
import ural.get_hostname

PATTERN_QUERY = re.compile(r"(?:format|type)\=(?:xml|feed|atom|rss)", re.I)
PATTERN_FILE_OBVIOUS = re.compile(
    r"(?:news|feed|rss|atom|index|blog)s?\.(?:xml|atom|rss|php|json)$", re.I
)
PATTERN_FILE = re.compile(r".+\.(?:rss|atom)")
PATTERN_KEYWORD = re.compile(
    r"(?:\/|\.|-|_)(?:rss|feed|atom)s?[0-9]*(((?:s|\/|\.|-|_))||^)", re.I
)


def should_be_rss_url(url):
    query = urlsplit(url).query
    path = list(reversed(urlpathsplit(url)))
    path = path[0:3:1]
    hostname = ural.get_hostname(url)

    if not hostname:
        return False
    if query and PATTERN_QUERY.findall(query):
        return True
    if path and PATTERN_FILE_OBVIOUS.findall(path[0]):
        return True
    if path and PATTERN_FILE.findall(path[0]):
        return True
    if PATTERN_KEYWORD.findall(url):
        return True
    return False
