# =============================================================================
# Ural Google-related heuristic functions
# =============================================================================
#
# Collection of functions related to Google urls.
#
import re
from ural.utils import urlsplit, SplitResult

AMP_QUERY_RE = re.compile(r'amp(_.+)=?', re.I)
AMP_SUFFIXES_RE = re.compile(r'(?:\.amp(?=\.html$)|\.amp/?$|(?<=/)amp/?$)', re.I)


def is_amp_url(url):
    if not isinstance(url, SplitResult):
        splitted = urlsplit(url)
    else:
        splitted = url

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
