# =============================================================================
# Ural Domain Name Getter
# =============================================================================
#
# Function returning an url's domain name.
#
from ural.utils import safe_urlsplit
from ural.has_special_host import is_special_host


def get_hostname(url):
    try:
        return safe_urlsplit(url).hostname or None
    except ValueError:
        return None


def get_hostname_prefixes(hostname):
    result = []

    if is_special_host(hostname):
        return [hostname]

    if hostname:
        domain_parts = hostname.split(".")

        for i in range(len(domain_parts)):
            result.append(".".join(domain_parts[i:]))

    return result
