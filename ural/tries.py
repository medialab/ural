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

        # TODO: we can skip adding the hostname if a shortest match
        # already exist in the Trie, to save up memory
        key = reversed(hostname.split('.'))
        return self.set(key, True)

    def match_url(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        key = reversed(url.hostname.split('.'))

        return bool(self.longest(key))
