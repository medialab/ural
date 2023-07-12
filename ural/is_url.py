# =============================================================================
# Ural Url Testing Function
# =============================================================================
#
# A function returning True if its argument is a url.
#
from ural.utils import safe_urlsplit
from ural.has_special_host import is_special_host
from ural.tld import has_valid_tld
from ural.patterns import (
    URL_RE,
    URL_WITH_PROTOCOL_RE,
    RELAXED_URL,
    RELAXED_URL_WITH_PROTOCOL_RE,
    HTTP_PROTOCOL_RE,
)


def is_url(
    string,
    require_protocol=True,
    tld_aware=False,
    allow_spaces_in_path=False,
    only_http_https=True,
):
    """
    Function returning True if its string argument is a url.

    Args:
        string (str): string to test.
        require_protocol (bool, optional): whether the argument has to have a
            protocol to be considered a url. Defaults to True.
        tld_aware (bool, optional): whether to check if the url's tld
            exists. Defaults to False.
        allow_spaces_in_path (bool, optional): whether to accept spaces in
            the url's path. Defaults to False.
        only_http_https (bool, optional): Whether to only allow http and https
            protocols. Defaults to True.

    Returns:
        bool: True if the argument is a url, False if not.

    """
    string = string.strip()

    if not string:
        return False

    if require_protocol:

        if only_http_https and not HTTP_PROTOCOL_RE.match(string):
            return False

        if allow_spaces_in_path:
            pattern = RELAXED_URL_WITH_PROTOCOL_RE
        else:
            pattern = URL_WITH_PROTOCOL_RE
    else:
        if allow_spaces_in_path:
            pattern = RELAXED_URL
        else:
            pattern = URL_RE

    if not pattern.match(string):
        return False

    if tld_aware:
        parsed = safe_urlsplit(string)
        if not has_valid_tld(parsed):
            return is_special_host(parsed.hostname)

    return True
