# =============================================================================
# Ural Could Be HTML Function
# =============================================================================
#
# A function returning whether the given url could point to a HTML document.
#
from os.path import splitext
from ural.utils import safe_urlsplit

HTML_LIKE_EXTENSIONS = {
    ".htm",
    ".html",
    ".dhtml",
    ".shtml",
    ".xhtml",
    ".asp",
    ".aspx",
    ".jsp",
    ".jspx",
    ".pl",
    ".php",
    ".php5",
    ".cgi",
    ".bin",
}


def could_be_html(url):
    path = safe_urlsplit(url).path

    _, ext = splitext(path)

    if not ext:
        return True

    return ext in HTML_LIKE_EXTENSIONS
