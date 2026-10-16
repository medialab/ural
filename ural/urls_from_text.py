# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Extraction Function
# =============================================================================
#
# A function returning an iterator over the urls present in the string argument.
#
import re

from ural.patterns import URL_IN_TEXT_RE

IRRELEVANT_PUNCTUATION = set("!?#\"$%&'*+,-.:;<=>@[\\]^_`{|}~…’‘`‛«»„‟“”-‐‒–—―−‑⁃,،、")
PARTS_RE = re.compile(r",(?=https?://)")


def urls_from_text(string):
    """
    Function returning an iterator over the urls present in the string argument.

    Args:
        string (str): source string.

    Yields:
        str: an url.

    """
    for match in re.finditer(URL_IN_TEXT_RE, string):
        url = match.group(0)
        s = match.start()

        if s > 0:
            if string[s - 1] == "[" and "](" in url:
                remainder, url = url.split("](", 1)
                url = url.rsplit(")", 1)[0]
                yield remainder.strip()

            elif string[s - 1] == "(":
                url = url.rsplit(")", 1)[0]

        last_punct = None

        stop = len(url) - 1
        i = stop

        while i != 0 and url[i] in IRRELEVANT_PUNCTUATION and url[i] != last_punct:
            last_punct = url[i]
            i -= 1

        if i != stop:
            url = url[: i + 1]

        yield from PARTS_RE.split(url)
