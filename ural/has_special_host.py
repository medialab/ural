# -*- coding: utf-8 -*-
# =============================================================================
# Ural Has Special Host Function
# =============================================================================
#
# Function returning whether the given url looks like it has a special host.
#

from ural.utils import safe_urlsplit
from ural.is_special_host import is_special_host


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
