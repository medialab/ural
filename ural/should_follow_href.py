# =============================================================================
# Ural Should Follow Href Function
# =============================================================================
#
# A function returning whether the given href attribute of a html <a> tag
# should be followed.
#

# NOTE: one should also compare the joined url to the current one usually
def should_follow_href(href):
    href = href.strip()

    if not href or href.startswith("#"):
        return False

    if ":" in href:
        return href.startswith("http:") or href.startswith("https:")

    return True
