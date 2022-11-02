# -*- coding: utf-8 -*-
# =============================================================================
# Ural Is Special Host Function
# =============================================================================
#
# Function returning whether the given domain looks like a special host.
#

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
