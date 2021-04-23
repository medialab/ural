# =============================================================================
# Ural Tries
# =============================================================================
#
# Collection of specialized Tries used with urls.
#
from phylactery import TrieDict

from ural.utils import safe_urlsplit


# NOTE: this trie currently has undefined behavior with some special hosts
class HostnameTrieSet(TrieDict):
    def add(self, hostname):
        key = list(reversed(hostname.split('.')))

        # If a shortest key already exist, we can trim the subdomain
        if self.longest(key) is not None:
            return

        self.set(key, True)

    def match(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        key = reversed(url.hostname.split('.'))

        return bool(self.longest(key))
