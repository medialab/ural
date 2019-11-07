# =============================================================================
# Ural Youtube-related heuristic functions
# =============================================================================
#
# Collection of functions related to Youtube urls.
#
import re
try:
    from urllib.parse import urlsplit, SplitResult
except ImportError:
    from urlparse import urlsplit, SplitResult

from ural.ensure_protocol import ensure_protocol

YOUTUBE_DOMAIN_PATTERN = re.compile(r'(?:youtube(?:\.googleapis)?\.[^.]+$|youtu\.be$)', re.I)


def is_youtube_url(url):
    if isinstance(url, SplitResult):
        parsed = url
    else:
        url = ensure_protocol(url)
        parsed = urlsplit(url)

    return bool(re.search(YOUTUBE_DOMAIN_PATTERN, parsed.hostname))
