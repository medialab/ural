# =============================================================================
# Ural Domain Name Getter
# =============================================================================
#
# Function returning an url's domain name.
#
from tld import get_fld


def get_domain_name(url):
    """
    Function returning the given url's domain name as a string. This function
    is of course TLD aware.

    Args:
        url (string): Target url.

    Returns:
        str: the url's domain name.

    """
    return get_fld(url, fix_protocol=True, fail_silently=True)
