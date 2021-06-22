# =============================================================================
# Ural Tries
# =============================================================================
#
# Collection of specialized Tries used with urls.
#
from phylactery import TrieDict

from ural.utils import safe_urlsplit, decode_punycode_hostname


def tokenize_hostname(hostname):
    return reversed(decode_punycode_hostname(hostname).strip().lower().split('.'))


def join_hostname(key):
    return '.'.join(reversed(key))


# NOTE: this trie currently has undefined behavior with some special hosts
class HostnameTrieSet(TrieDict):
    def __init__(self):
        super(HostnameTrieSet, self).__init__(list)

    def add(self, hostname):
        key = list(tokenize_hostname(hostname))

        # If a shortest key already exist, we can trim the subdomain
        if self.longest(key) is not None:
            return

        self.set(key, True)

    def match(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        key = tokenize_hostname(url.hostname)

        return bool(self.longest(key))

    def __iter__(self):
        for key in super(HostnameTrieSet, self).keys():
            yield join_hostname(key)
