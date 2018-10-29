# =============================================================================
# Ural URL Ensure Protocol Function
# =============================================================================
#
# A function checking if the url features a protocol, and adding one if there is none.
#
import re

PROTOCOL_RE = re.compile('^[^:]*:?//')


def ensure_protocol(url, protocol='http'):
    if not PROTOCOL_RE.match(url):
        url = protocol + '://' + url
    elif url[:2] == '//':
        url = protocol + ':' + url
    return url
