from ural.data import ISO_3166_1_COUNTRIES_ALPHA_2
from ural.normalize_url import normalize_url, normalize_hostname
from ural.utils import SplitResult, urlunsplit, urlsplit, unsplit_netloc
from ural.infer_redirection import infer_redirection as resolve
from ural.ensure_protocol import ensure_protocol
from ural.tld import split_suffix

LANG_QUERY_KEYS = ("gl", "hl")

# TODO: drop tld


def lang_query_item_filter(key, _):
    return key not in LANG_QUERY_KEYS


def strip_lang_subdomains_from_hostname(hostname):
    if hostname.count(".") > 1:
        subdomain, remaining_hostname = hostname.split(".", 1)
        if len(subdomain) == 5 and "-" in subdomain:
            lang, country = subdomain.split("-", 1)
            if len(lang) == 2 and len(country) == 2:
                if (
                    lang.upper() in ISO_3166_1_COUNTRIES_ALPHA_2
                    and country.upper() in ISO_3166_1_COUNTRIES_ALPHA_2
                ):
                    hostname = remaining_hostname
        elif len(subdomain) == 2:
            if subdomain.upper() in ISO_3166_1_COUNTRIES_ALPHA_2:
                hostname = remaining_hostname

    return hostname


def fingerprint_hostname(hostname, strip_suffix=False):
    hostname = normalize_hostname(hostname)

    if strip_suffix:
        # TODO: this is not performant because the code path reparses again
        r = split_suffix(hostname)

        if r is not None:
            hostname, _ = r

    return strip_lang_subdomains_from_hostname(hostname)


def get_fingerprinted_hostname(url, infer_redirection=True, strip_suffix=False):
    if infer_redirection:
        url = resolve(url)

    if isinstance(url, SplitResult):
        splitted = url
    else:
        try:
            splitted = urlsplit(ensure_protocol(url.strip()))
        except ValueError:
            return None

    if not splitted.hostname:
        return None

    return fingerprint_hostname(splitted.hostname, strip_suffix=strip_suffix)


def fingerprint_url(url, unsplit=True, strip_suffix=False, platform_aware=False):
    url = url.lower()

    splitted = normalize_url(
        url,
        unsplit=False,
        query_item_filter=lang_query_item_filter,
        platform_aware=platform_aware,
    )
    _, netloc, path, query, fragment = splitted

    user, password, hostname, port = (
        splitted.username,
        splitted.password,
        splitted.hostname,
        splitted.port,
    )

    if hostname:
        hostname = strip_lang_subdomains_from_hostname(hostname)

        if strip_suffix:
            # TODO: this is not performant because the code path reparses again
            r = split_suffix(hostname)

            if r is not None:
                hostname, _ = r

    # Dropping port
    port = None

    netloc = unsplit_netloc(user, password, hostname, port)

    result = SplitResult("", netloc, path, query, fragment)

    if not unsplit:
        return result

    return urlunsplit(result)[2:]
