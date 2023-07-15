from ural.data import ISO_3166_1_COUNTRIES_ALPHA_2
from ural.normalize_url import normalize_url, normalize_hostname
from ural.utils import SplitResult, urlunsplit, urlsplit
from ural.infer_redirection import infer_redirection as resolve
from ural.ensure_protocol import ensure_protocol

LANG_QUERY_KEYS = ("gl", "hl")

# TODO: drop tld


def lang_query_item_filter(key, _):
    return key not in LANG_QUERY_KEYS


def strip_lang_subdomains_from_netloc(netloc):
    if netloc.count(".") > 1:
        subdomain, remaining_netloc = netloc.split(".", 1)
        if len(subdomain) == 5 and "-" in subdomain:
            lang, country = subdomain.split("-", 1)
            if len(lang) == 2 and len(country) == 2:
                if (
                    lang.upper() in ISO_3166_1_COUNTRIES_ALPHA_2
                    and country.upper() in ISO_3166_1_COUNTRIES_ALPHA_2
                ):
                    netloc = remaining_netloc
        elif len(subdomain) == 2:
            if subdomain.upper() in ISO_3166_1_COUNTRIES_ALPHA_2:
                netloc = remaining_netloc

    return netloc


def fingerprint_hostname(hostname):
    hostname = normalize_hostname(hostname)

    return strip_lang_subdomains_from_netloc(hostname)


def get_fingerprinted_hostname(url, infer_redirection=True):
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

    return fingerprint_hostname(splitted.hostname)


def fingerprint_url(url, unsplit=True):
    url = url.lower()

    splitted = normalize_url(
        url, unsplit=False, query_item_filter=lang_query_item_filter
    )
    _, netloc, path, query, fragment = splitted

    netloc = strip_lang_subdomains_from_netloc(netloc)

    result = SplitResult("", netloc, path, query, fragment)

    if not unsplit:
        return result

    return urlunsplit(result)[2:]
