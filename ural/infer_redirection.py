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

OBVIOUS_REDIRECTS_RE = re.compile(
    QUERY_VALUE_IN_URL_TEMPLATE
    % r"(?:redirect(?:_to)?|target|redir|next|link|orig|goto|url|[luq])",
    re.I,
)
REDIRECTION_DOMAINS_RE = re.compile(
    r"(?:\.ampproject\.org/[cv]/(?:s/)?|bc\.marfeelcache\.com/amp/|bc\.marfeel\.com/)",
    re.I,
)


def infer_redirection(url, recursive=True):
    """
    Function returning the url that the given url will redirect to. This is done
    by finding obvious hints in the GET parameters that the given url is in
    fact a redirection.

    Args:
        url (string): Target url.
        recursive (bool): Whether to apply the function recursively until
            no redirection can be inferred. Defaults to `True`.

    Returns:
        string: Redirected url or the original url if nothing was found.
    """

    redirection_split = REDIRECTION_DOMAINS_RE.split(url, 1)

    target = None

    if len(redirection_split) > 1:
        target = "https://" + redirection_split[1]

    else:
        obvious_redirect_match = re.search(OBVIOUS_REDIRECTS_RE, url)

        if obvious_redirect_match is not None:
            potential_target = unquote(obvious_redirect_match.group(1))

            if potential_target.startswith("http://") or potential_target.startswith(
                "https://"
            ):
                target = potential_target

            if potential_target.startswith("/"):
                target = urljoin(url, potential_target)

    if target is None:
        return url

    if recursive:
        return infer_redirection(target, recursive=True)

    return target
