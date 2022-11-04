# =============================================================================
# Ural LRU Serialization Functions
# =============================================================================
#
# Functions related to LRU serialization.
#
import re

SERIALIZED_LRU_SPLITTER_RE = re.compile(r"\|(?=[shtpqfuw]:)")


def serialize_lru(stems):
    return "|".join(stems) + "|"


def unserialize_lru(lru):
    lru = lru.rstrip("|")
    return SERIALIZED_LRU_SPLITTER_RE.split(lru)
