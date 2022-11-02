# =============================================================================
# Ural Hostname Trie Set
# =============================================================================
#
# Hostname-aware custom implementation of a prefix trie used to efficiently
# match large numbers of domains.
#
from ural.classes import TrieDict
from ural.utils import safe_urlsplit, decode_punycode_hostname


def tokenize_hostname(hostname):
    return reversed(decode_punycode_hostname(hostname).strip().lower().split('.'))


def join_hostname(prefix):
    return '.'.join(reversed(prefix))


# NOTE: this trie currently has undefined behavior with some special hosts
class HostnameTrieSet(TrieDict):
    def __init__(self):
        super(HostnameTrieSet, self).__init__()

    def add(self, hostname):
        prefix = list(tokenize_hostname(hostname))

        # If a shortest prefix already exist, we can trim the subdomain
        if self.longest_matching_prefix_value(prefix) is not None:
            return

        self[prefix] = True

    def match(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        prefix = tokenize_hostname(url.hostname)

        return bool(self.longest_matching_prefix_value(prefix))

    def __iter__(self):
        for prefix in super(HostnameTrieSet, self).prefixes():
            yield join_hostname(prefix)
