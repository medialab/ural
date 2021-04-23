# =============================================================================
# Ural Tries
# =============================================================================
#
# Collection of specialized Tries used with urls.
#
from phylactery import TrieDict

from ural.utils import safe_urlsplit


class HostnameTrieSet(TrieDict):
    def add(self, hostname):
        key = reversed(hostname.split('.'))
        return self.set(key, True)

    def match_url(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        key = reversed(url.hostname.split('.'))

        return bool(self.longest(key))
