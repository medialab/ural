# =============================================================================
# Ural Redirecion Inferrence Function
# =============================================================================
#
# A lot of urls contains an obvious hint that they will in fact trigger
# a redirection. This modules gathers routines aimed at discovering
# those redirections without even firing a HTTP request.
#
import re

from ural.patterns import QUERY_VALUE_IN_URL_TEMPLATE
from ural.utils import unquote, urljoin

OBVIOUS_REDIRECTS_RE = re.compile(QUERY_VALUE_IN_URL_TEMPLATE % r'(?:redirect(?:_to)?|next|url|[lu])', re.I)
REDIRECTION_DOMAINS_RE = re.compile(r'(?:\.ampproject\.org/[cv]/(?:s/)?|bc\.marfeelcache\.com/amp/|bc\.marfeel\.com/)', re.I)


def infer_redirection(url):
    """
    Function returning the url that the given url will redirect to. This is done
    by finding obvious hints in the GET parameters that the given url is in
    fact a redirection.

    Args:
        url (string): Target url.

    Returns:
        string: Redirected url or the original url if nothing was found.
    """

    redirection_split = REDIRECTION_DOMAINS_RE.split(url, 1)

    if len(redirection_split) > 1:
        return infer_redirection('https://' + redirection_split[1])

    obvious_redirect_match = re.search(OBVIOUS_REDIRECTS_RE, url)

    if obvious_redirect_match is not None:
        target = unquote(obvious_redirect_match.group(1))

        if target.startswith('http://') or target.startswith('https://'):
            return target

        if target.startswith('/'):
            return urljoin(url, target)

    return url
