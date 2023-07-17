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

if PY2:

    # NOTE: py2 version is not unicode-aware of course...
    def isprintable(string):
        return all(c >= " " for c in string)

else:
    isprintable = str.isprintable


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


def _generate_unquoted_parts(string, only_printable=False):
    previous_match_end = 0
    for ascii_match in ASCII_RE.finditer(string):
        start, end = ascii_match.span()
        yield string[previous_match_end:start]  # Non-ASCII
        # The ascii_match[1] group == string[start:end].

        m = ascii_match.group(1)
        c = _unquote_impl(m).decode("utf-8", "replae")

        if only_printable and not isprintable(c):
            yield m
        else:
            yield c

        previous_match_end = end
    yield string[previous_match_end:]  # Non-ASCII tail


def unquote(string, only_printable=False):
    if "%" not in string:
        return string

    return "".join(_generate_unquoted_parts(string, only_printable=only_printable))


__all__ = ["unquote"]
