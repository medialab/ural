# =============================================================================
# Ural Redirecion Inferrence Function
# =============================================================================
#
# A lot of urls contains an obvious hint that they will in fact trigger
# a redirection. This modules gathers routines aimed at discovering
# those redirections without even firing a HTTP request.
#


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
    pass
