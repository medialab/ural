# -*- coding: utf-8 -*-
# =============================================================================
# Ural Has Special Host Function
# =============================================================================
#
# Function returning whether the given url looks like it has a special host.
#

from ural.utils import safe_urlsplit
from ural.patterns import SPECIAL_HOSTS_RE


def is_special_host(hostname):
    """
    Function returning whether the given hostname looks like a special host.

    Args:
        hostname (str): hostname to test.

    Returns:
        bool

    """
    return bool(SPECIAL_HOSTS_RE.match(hostname))


def has_special_host(url):
    """
    Function returning whether the given url looks like it has a special host.

    Args:
        url (str): url to test.

    Returns:
        bool

    """
    parsed = safe_urlsplit(url)

    return is_special_host(parsed.hostname)
