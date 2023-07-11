# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Be RSS URL
# =============================================================================
#
# Function returning whether the given url should be a rss feed url.
#
import re

from ural.utils import safe_urlsplit, pathsplit
from ural.get_hostname import get_hostname

QUERY_RE = re.compile(r"(?:format|type)\=(?:xml|feed|atom|rss)", re.I)
FILE_OBVIOUS_RE = re.compile(
    r"(?:news|feeds?|rss|atoms?|index|blogs?)\.(?:xml|atom|rss|php|json)$", re.I
)
FILE_RE = re.compile(r".+\.(?:rss|atom)$")
KEYWORD_RE = re.compile(
    r"[\/\.\-_](?:rss|feeds?|atom)[0-9]*(((?:s|\/|\.|-|_))||^)", re.I
)


def could_be_rss(url):
    urlsplited = safe_urlsplit(url)
    query = urlsplited.query
    path = list(reversed(pathsplit(urlsplited.path)))
    hostname = get_hostname(url)

    if not hostname:
        return False
    if query and QUERY_RE.search(query):
        return True
    if path and FILE_OBVIOUS_RE.search(path[0]):
        return True
    if path and FILE_RE.search(path[0]):
        return True
    if KEYWORD_RE.search(url):
        return True
    return False
