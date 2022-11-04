# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Homepage Function
# =============================================================================
#
# Function returning whether the given url looks like a website's homepage.
#
from os.path import splitext

from ural.utils import safe_urlsplit

HOMEPAGE_PATHS = ["", "/", "/index", "/home"]


def is_homepage(url):
    """
    Function returning whether the given url looks like a website's homepage.

    Args:
        url (str): url to test.

    Returns:
        bool

    """
    parsed = safe_urlsplit(url)
    path = parsed.path.strip().rstrip("/")
    path, _ = splitext(path)

    return path in HOMEPAGE_PATHS
