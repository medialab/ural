# =============================================================================
# Ural LRU Module
# =============================================================================
#
# Module gathering LRU-related functions.
#
from ural.utils import string_type, urlunsplit
from ural.lru.serialization import serialize_lru, unserialize_lru
from ural.lru.stems import lru_stems, normalized_lru_stems
from ural.lru.trie import LRUTrie, NormalizedLRUTrie


def url_to_lru(url, suffix_aware=False):
    return serialize_lru(lru_stems(url, suffix_aware=suffix_aware))


def lru_to_url(lru):

    # Handling both stems and serialized lru
    if isinstance(lru, string_type):
        stems = unserialize_lru(lru)
    else:
        stems = lru

    # Indexing stems
    stems_index = {}

    for stem in stems:
        tag, value = stem.split(":", 1)

        if tag == "h" and tag in stems_index:
            stems_index[tag] = value + "." + stems_index[tag]
        elif tag == "p" and tag in stems_index:
            stems_index[tag] += "/" + value
        else:
            stems_index[tag] = value

    # Building the url back
    scheme = stems_index.get("s", "")
    auth = stems_index.get("u", "")

    w = stems_index.get("w")

    if w is not None:
        auth += ":" + w

    netloc = ""

    if auth:
        netloc = auth + "@"

    netloc += stems_index.get("h", "")

    t = stems_index.get("t")

    if t is not None:
        netloc += ":" + t

    p = stems_index.get("p")

    path = ""

    if p is not None:
        path = "/" + p

    query = stems_index.get("q", "")
    fragment = stems_index.get("f", "")

    return urlunsplit((scheme, netloc, path, query, fragment))


__all__ = [
    "serialize_lru",
    "unserialize_lru",
    "lru_stems",
    "normalized_lru_stems",
    "LRUTrie",
    "NormalizedLRUTrie",
    "url_to_lru",
    "lru_to_url",
]
