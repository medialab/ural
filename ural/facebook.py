# =============================================================================
# Ural Facebook-related heuristic functions
# =============================================================================
#
# Collection of functions crafted to work with Facebook's urls.
#
import re
from urllib.parse import urlsplit, urlunsplit
from ural.ensure_protocol import ensure_protocol

MOBILE_REPLACE_RE = re.compile(r'^([^.]+\.)?facebook\.', re.I)


def convert_facebook_url_to_mobile(url):
    """
    Function parsing the given facebook url and returning the same but for
    the mobile website.
    """
    safe_url = ensure_protocol(url)

    has_protocol = safe_url == url

    scheme, netloc, path, query, fragment = urlsplit(safe_url)

    if 'facebook' not in netloc:
        raise Exception('ural.facebook.convert_facebook_url_to_mobile: %s is not a facebook url' % url)

    netloc = re.sub(MOBILE_REPLACE_RE, 'm.facebook.', netloc)

    result = (
        scheme,
        netloc,
        path,
        query,
        fragment
    )

    result = urlunsplit(result)

    if not has_protocol:
        result = result.split('://', 1)[-1]

    return result
