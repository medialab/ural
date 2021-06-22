# =============================================================================
# Ural Domain Name Getter
# =============================================================================
#
# Function returning an url's domain name.
#
from tld import get_fld
from ural.utils import urlsplit
from ural.ensure_protocol import ensure_protocol


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


def get_hostname(url):
    try:
        return urlsplit(ensure_protocol(url)).hostname or None
    except ValueError:
        return None


def get_hostname_prefixes(hostname):
    result = []

    if hostname:
        domain_parts = hostname.split('.')

        for i in range(len(domain_parts)):
            result.append('.'.join(domain_parts[i:]))

    return result
