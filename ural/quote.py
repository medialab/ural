# NOTE: it would be nice to handle quoting recursivity

from __future__ import unicode_literals
from platform import python_version_tuple

PY2 = python_version_tuple()[0] == "2"

import re
from functools import partial

from ural.utils import quote

# NOTE: the following code for `unquote` is adapted from cpython:
# https://github.com/python/cpython/blob/main/Lib/urllib/parse.py
HEX = "0123456789ABCDEFabcdef"
if PY2:
    HEX_TO_BYTE = {(a + b).encode(): chr(int(a + b, 16)) for a in HEX for b in HEX}
else:
    HEX_TO_BYTE = {(a + b).encode(): bytes.fromhex(a + b) for a in HEX for b in HEX}

ASCII_RE = re.compile("([\x00-\x7f]+)")


def _unquote_impl(string, only_printable=False, unsafe=None):
    string = string.encode("utf-8")
    bits = string.split(b"%")
    if len(bits) == 1:
        return string
    res = bytearray(bits[0])
    append = res.extend

    for item in bits[1:]:
        b = HEX_TO_BYTE.get(item[:2])

        if b is not None:
            if only_printable and b < b" ":
                append(b"%")
                append(item)
            elif unsafe is not None and b in unsafe:
                append(b"%")
                append(item)
            else:
                append(b)
                append(item[2:])
        else:
            append(b"%")
            append(item)

    return res


def _generate_unquoted_parts(string, only_printable=False, unsafe=None):
    previous_match_end = 0
    for ascii_match in ASCII_RE.finditer(string):
        start, end = ascii_match.span()
        yield string[previous_match_end:start]  # Non-ASCII
        # The ascii_match[1] group == string[start:end].

        m = ascii_match.group(1)
        c = _unquote_impl(m, only_printable=only_printable, unsafe=unsafe).decode(
            "utf-8", "replace"
        )

        yield c

        previous_match_end = end
    yield string[previous_match_end:]  # Non-ASCII tail


# NOTE: here, unsafe must be a container of bytes
def unquote(string, only_printable=False, unsafe=None, normalize_space=False):
    if "%" not in string:
        return string

    q = "".join(
        _generate_unquoted_parts(string, only_printable=only_printable, unsafe=unsafe)
    )

    if normalize_space:
        q = q.replace(" ", "%20")

    return q


# NOTE: to safely unquote we don't need to replace invalid character because it would
# imply that the parsed url was invalid from the start (except for spaces)

UNSAFE_FOR_AUTH_ITEM = b" @:"
UNSAFE_FOR_PATH = b" ?#"
UNSAFE_FOR_QUERY_ITEM = b" &=#"
UNSAFE_FOR_FRAGMENT = b" "

# NOTE: those method should only be used on parsed urls to canonicalize/normalize.
safely_unquote_auth_item = partial(
    unquote, only_printable=True, normalize_space=True, unsafe=UNSAFE_FOR_AUTH_ITEM
)
safely_unquote_path = partial(
    unquote, only_printable=True, normalize_space=True, unsafe=UNSAFE_FOR_PATH
)
safely_unquote_query_item = partial(
    unquote, only_printable=True, normalize_space=True, unsafe=UNSAFE_FOR_QUERY_ITEM
)
safely_unquote_fragment = partial(
    unquote, only_printable=True, normalize_space=True, unsafe=UNSAFE_FOR_FRAGMENT
)


def safely_unquote_qsl(qsl):
    return [
        (
            safely_unquote_query_item(key),
            safely_unquote_query_item(value) if value is not None else None,
        )
        for key, value in qsl
    ]


QUOTED_SPLIT_RE = re.compile(r"(%[0-9A-Fa-f]{2})")
QUOTED_RE = re.compile(r"^%[0-9A-Fa-f]{2}$")


def safely_quote_iter(string):
    for piece in QUOTED_SPLIT_RE.split(string):
        if QUOTED_RE.match(piece):
            yield piece
        else:
            yield quote(piece)


def safely_quote(string):
    return "".join(safely_quote_iter(string))


def safely_quote_qsl(qsl):
    return [
        (safely_quote(key), safely_quote(value) if value is not None else None)
        for key, value in qsl
    ]


def upper_match(match):
    return match.group(0).upper()


LOWERCASE_QUOTED_RE = re.compile(r"%(?:[0-9A-F][a-f]|[a-f][0-9A-F]|[a-f]{2})")


def upper_quoted(string):
    return LOWERCASE_QUOTED_RE.sub(upper_match, string)


__all__ = [
    "unquote",
    "safely_unquote_auth",
    "safely_unquote_path",
    "safely_unquote_query_item",
    "safely_unquote_fragment",
    "safely_unquote_qsl",
    "safely_quote",
    "safely_quote_qsl",
    "upper_quoted",
]
