from __future__ import unicode_literals
from platform import python_version_tuple

PY2 = python_version_tuple()[0] == "2"

import re

# NOTE: the following code for `unquote` is adapted from cpython:
# https://github.com/python/cpython/blob/main/Lib/urllib/parse.py
HEX = "0123456789ABCDEFabcdef"
if PY2:
    HEX_TO_BYTE = {(a + b).encode(): chr(int(a + b, 16)) for a in HEX for b in HEX}
else:
    HEX_TO_BYTE = {(a + b).encode(): bytes.fromhex(a + b) for a in HEX for b in HEX}

ASCII_RE = re.compile("([\x00-\x7f]+)")


def _unquote_impl(string):
    string = string.encode("utf-8")
    bits = string.split(b"%")
    if len(bits) == 1:
        return string
    res = bytearray(bits[0])
    append = res.extend

    for item in bits[1:]:
        try:
            append(HEX_TO_BYTE[item[:2]])  # type: ignore
            append(item[2:])
        except KeyError:
            append(b"%")
            append(item)
    return res


def _generate_unquoted_parts(string):
    previous_match_end = 0
    for ascii_match in ASCII_RE.finditer(string):
        start, end = ascii_match.span()
        yield string[previous_match_end:start]  # Non-ASCII
        # The ascii_match[1] group == string[start:end].
        yield _unquote_impl(ascii_match.group(1)).decode("utf-8", "replae")
        previous_match_end = end
    yield string[previous_match_end:]  # Non-ASCII tail


def unquote(string):
    if "%" not in string:
        return string

    return "".join(_generate_unquoted_parts(string))


__all__ = ["unquote"]
