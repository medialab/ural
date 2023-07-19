# =============================================================================
# Ural Should Follow Href Function
# =============================================================================
#
# A function returning whether the given href attribute of a html <a> tag
# should be followed.
#
import re

HTTP_PROTOCOL_RE = re.compile(r'^https?://', re.I)

# NOTE: one should also compare the joined url to the current one usually
def should_follow_href(href):
    href = href.strip()

    if not href or href.startswith("#"):
        return False

    if ":" in href:
        return bool(HTTP_PROTOCOL_RE.match(href))

    return True
