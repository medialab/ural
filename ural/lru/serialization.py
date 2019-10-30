# =============================================================================
# Ural LRU Serialization Functions
# =============================================================================
#
# Functions related to LRU serialization.
#


def serialize_lru(stems):
    return '|'.join(stems) + '|'


def unserialize_lru(serial):
    serial = serial.rstrip('|')
    return serial.split('|')
