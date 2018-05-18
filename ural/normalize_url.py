# =============================================================================
# Ural URL Normalization Function
# =============================================================================
#
# A handy function relying on heuristics to find and drop irrelevant or
# non-discriminant parts of a URL.
#
import re
from os.path import splitext
from furl import furl

IRRELEVANT_QUERY_RE = re.compile('^utm_(?:term|medium|source|campaign|content)|xtor$')
IRRELEVANT_SUBDOMAIN_RE = re.compile('^(?:www\\d?|mobile|m)\\.')


def normalize_url(url, drop_trailing_slash=True):
    """
    Function normalizing the given url by stripping it of usually
    non-discriminant parts such as irrelevant query items or sub-domains etc.

    This is a very useful utility when attempting to match similar urls
    written slightly differently when shared on social media etc.

    Args:
        url (str): Target URL as a string.
        drop_trailing_slash (bool, optional): Whether to drop trailing slash.
            Defaults to `True`.

    Returns:
        string: The normalized url.

    """

    f = furl(url)
    path = f.path

    # Normalizing the path
    path.normalize()

    # Dropping trailing slash
    if drop_trailing_slash and \
       len(path.segments) != 0 and \
       path.segments[-1] == '':
        path.segments = path.segments[:-1]

    # Dropping 'index'
    if len(path.segments) != 0:
        last_segment = path.segments[-1]
        filename, ext = splitext(last_segment)

        if filename == 'index':
            path.segments = path.segments[:-1]

    # Dropping irrelevant query items
    # NOTE: if no query is present, ? will be dropped
    query = f.query.params
    query_items_to_delete = []

    for key in query.keys():
        if IRRELEVANT_QUERY_RE.match(key):
            query_items_to_delete.append(key)

    for query_item_to_delete in query_items_to_delete:
        del query[query_item_to_delete]

    # Dropping fragment if it's not routing
    fragment = f.fragment

    if len(fragment.path.segments) <= 1:
        f.remove(fragment=True)

    # Dropping irrelevant subdomains
    if f.host:
        f.host = re.sub(IRRELEVANT_SUBDOMAIN_RE, '', f.host)

    # Dropping scheme
    f.scheme = None

    if drop_trailing_slash:
        return f.url.rstrip('/')
    else:
        return f.url
