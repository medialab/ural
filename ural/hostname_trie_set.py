# =============================================================================
# Ural Hostname Trie Set
# =============================================================================
#
# Hostname-aware custom implementation of a prefix trie used to efficiently
# match large numbers of domains.
#
from ural.classes import TrieDict
from ural.utils import safe_urlsplit, decode_punycode_hostname
from ural.has_special_host import is_special_host


def tokenize_hostname(hostname):
    if is_special_host(hostname):
        return [hostname]

    hostname = hostname.strip().lower()
    hostname_parts = decode_punycode_hostname(hostname, as_parts=True)

    return reversed(hostname_parts)


def join_hostname(prefix):
    return ".".join(reversed(prefix))


# NOTE: this trie currently has undefined behavior with some special hosts
class HostnameTrieSet(object):
    def __init__(self):
        self.__trie = TrieDict()

    def __len__(self):
        return len(self.__trie)

    def add(self, hostname):

        prefix = list(tokenize_hostname(hostname))

        self.__trie.set_and_prune_if_shorter(prefix, True)

    def match(self, url):
        url = safe_urlsplit(url)

        if not url.hostname:
            return False

        prefix = tokenize_hostname(url.hostname)

        return bool(self.__trie.longest_matching_prefix_value(prefix))

    def __iter__(self):
        for prefix in self.__trie.prefixes():
            yield join_hostname(prefix)
