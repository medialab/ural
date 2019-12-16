# =============================================================================
# Ural Google-related heuristic functions
# =============================================================================
#
# Collection of functions related to Google urls.
#
import re
from ural.utils import safe_urlsplit, unquote
from ural.patterns import QUERY_VALUE_IN_URL_TEMPLATE

AMP_QUERY_RE = re.compile(r'amp(_.+)=?', re.I)
AMP_SUFFIXES_RE = re.compile(r'(?:\.amp(?=\.html$)|\.amp/?$|(?<=/)amp/?$)', re.I)

URL_EXTRACT_RE = re.compile(QUERY_VALUE_IN_URL_TEMPLATE % r'url')


def is_amp_url(url):
    splitted = safe_urlsplit(url)

    if splitted.hostname.endswith('.ampproject.org'):
        return True

    if splitted.hostname.startswith('amp-'):
        return True

    if splitted.hostname.startswith('amp.'):
        return True

    if '/amp/' in splitted.path:
        return True

    if AMP_SUFFIXES_RE.search(splitted.path):
        return True

    if splitted.query and AMP_QUERY_RE.search(splitted.query):
        return True

    return False


def is_google_link(url):
    splitted = safe_urlsplit(url)

    if not splitted.hostname or 'google.' not in splitted.hostname:
        return False

    if splitted.path != '/url':
        return False

    return True


def extract_url_from_google_link(url):
    m = URL_EXTRACT_RE.search(url)

    if m is None:
        return None

    return unquote(m.group(1))
