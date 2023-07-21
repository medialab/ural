# =============================================================================
# Ural URL Normalization Function
# =============================================================================
#
# A handy function relying on heuristics to find and drop irrelevant or
# non-discriminant parts of a URL.
#
import re
from os.path import splitext

from ural.ensure_protocol import ensure_protocol
from ural.infer_redirection import infer_redirection as resolve
from ural.utils import (
    safe_qsl_iter,
    safe_serialize_qsl,
    urlsplit,
    urlunsplit,
    unsplit_netloc,
    decode_punycode_hostname,
    normpath,
    fix_common_query_mistakes,
    SplitResult,
)
from ural.quote import (
    safely_unquote_auth_item,
    safely_unquote_path,
    safely_unquote_qsl,
    safely_unquote_fragment,
    safely_quote,
    safely_quote_qsl,
    upper_quoted,
)
from ural.patterns import PROTOCOL_RE, CONTROL_CHARS_RE
from ural.facebook import is_facebook_url, parse_facebook_url
from ural.youtube import is_youtube_url, normalize_youtube_url

IRRELEVANT_QUERY_PATTERN = r"^(?:__twitter_impression|_guc_consent_skip|guccounter|fb_action_types|(?:php|asp|j)?sessionid|fb_action_ids|fb_source|echobox|feature|recruiter|_unique_id|twclid|mibextid|campaignid|adgroupid|cn-reloaded|ao_noptimize|mkt_tok|fbclid|igshid|refid|gclid|mc_cid|mc_eid|__tn__|_ft_|dclid|wpamp|fref|usqp|ncid|mtm_.+|utm_.+%s|s?een|cftoken|cfid|sid|xt(?:loc|ref|cr|np|or|s)|at_.+|_ga)$"

IRRELEVANT_SUBDOMAIN_PATTERN = r"\b(?:www\d?|mobile%s|m)\."

AMP_QUERY_PATTERN = r"|amp_.+|amp"
AMP_QUERY_COMBOS = {"outputtype": ("amp",)}
AMP_SUBDOMAIN_PATTERN = r"|amp"
AMP_SUFFIXES_RE = re.compile(r"(?:\.amp(?=\.html$)|\.amp/?$|(?<=/)amp/?$)", re.I)

IRRELEVANT_QUERY_RE = re.compile(IRRELEVANT_QUERY_PATTERN % r"", re.I)
IRRELEVANT_SUBDOMAIN_RE = re.compile(IRRELEVANT_SUBDOMAIN_PATTERN % r"", re.I)

IRRELEVANT_QUERY_AMP_RE = re.compile(IRRELEVANT_QUERY_PATTERN % AMP_QUERY_PATTERN, re.I)
IRRELEVANT_SUBDOMAIN_AMP_RE = re.compile(
    IRRELEVANT_SUBDOMAIN_PATTERN % AMP_SUBDOMAIN_PATTERN, re.I
)

IRRELEVANT_QUERY_COMBOS = {
    "marfeeltn": ("amp",),
    "mode": ("amp",),
    "output": ("amp",),
    "platform": ("hootsuite",),
    "fromref": ("twitter",),
    "m": (
        "0",
        "1",
    ),
    "ref": set(
        [
            "bookmark",
            "bookmarks",
            "distributor_share",
            "fb",
            "fb_i",
            "m_notif",
            "nf",
            "notif",
            "shortener",
            "ts",
            "tw",
            "tw_i",
            "twhr",
            "twhs",
            "twitter",
            "viral",
            "feed",
            "twtrec",
        ]
    ),
    "s": lambda v: len(v) <= 2 and all("0" <= x <= "9" for x in v),
    "source": ("twitter",),
    "sns": ("tw",),
    "spref": ("fb", "ts", "tw", "tw_i", "twitter"),
    "_ss": ("r",),
}

# NOTE: if this list becomes too long, switch to HostnameTrieMap
PER_DOMAIN_QUERY_FILTERS = [
    ("facebook.com", lambda k, v: k == "_rdc" or k == "_rdr"),
    (
        "youtube.com",
        lambda k, v: k == "t"
        or k == "si"
        or k == "cbrd"
        or k == "ucbcb"
        or k == "ab_channel",
    ),
]


def qsl_sort_key(item):
    return item[0], item[1] or "", 0 if item[1] is None else 1


def should_strip_query_item(
    item, normalize_amp=True, query_item_filter=None, domain_filter=None
):
    key = item[0].lower()

    pattern = IRRELEVANT_QUERY_AMP_RE if normalize_amp else IRRELEVANT_QUERY_RE

    if pattern.match(key):
        return True

    value = item[1]

    if key in IRRELEVANT_QUERY_COMBOS:
        result = IRRELEVANT_QUERY_COMBOS[key]
        if callable(result):
            return result(value)
        return value in IRRELEVANT_QUERY_COMBOS[key]

    # NOTE: only keep elif because query combos and amp query combos
    # are mutually exclusive.
    elif normalize_amp and key in AMP_QUERY_COMBOS:
        return value in AMP_QUERY_COMBOS[key]

    if domain_filter is not None:
        return domain_filter(key, value)

    if query_item_filter is not None:
        return not query_item_filter(key, value)

    return False


def should_strip_fragment(fragment):
    if fragment == "!/" or fragment == "/" or fragment == "!":
        return False

    return fragment.startswith("/") or fragment.startswith("!")


def normalize_hostname(hostname, normalize_amp=True):
    hostname = hostname.strip().lower()
    hostname = CONTROL_CHARS_RE.sub("", hostname)

    pattern = IRRELEVANT_SUBDOMAIN_AMP_RE if normalize_amp else IRRELEVANT_SUBDOMAIN_RE

    hostname = pattern.sub("", hostname)

    if normalize_amp and hostname.startswith("amp-"):
        hostname = hostname[4:]

    hostname = decode_punycode_hostname(hostname)

    return hostname


def get_normalized_hostname(url, normalize_amp=True, infer_redirection=True):
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

    return normalize_hostname(splitted.hostname, normalize_amp=normalize_amp)


# NOTE: normalize_url is not suited to be able to process already splitted urls,
# because of mutliple string preprocessing tricks and redirection inferrence
# NOTE: query filter run before quoting shenanigans because targeted pattern
# are not subject to escaping, usually
def normalize_url(
    url,
    sort_query=True,
    strip_authentication=True,
    strip_trailing_slash=True,
    strip_index=True,
    strip_protocol=True,
    strip_irrelevant_subdomains=True,
    strip_fragment="except-routing",
    normalize_amp=True,
    fix_common_mistakes=True,
    infer_redirection=True,
    platform_aware=False,
    # NOTE: following arguments currently undocumented
    unsplit=True,
    quoted=False,
    query_item_filter=None,
):
    """
    Function normalizing the given url by stripping it of usually
    non-discriminant parts such as irrelevant query items or sub-domains etc.

    This is a very useful utility when attempting to match similar urls
    written slightly differently when shared on social media etc.

    Args:
        url (str): Target URL as a string.
        sort_query (bool, optional): Whether to sort query items or not.
            Defaults to `True`.
        strip_authentication (bool, optional): Whether to drop authentication.
            Defaults to `True`.
        strip_trailing_slash (bool, optional): Whether to drop trailing slash.
            Defaults to `False`.
        strip_index (bool, optional): Whether to drop trailing index at the end
            of the url. Defaults to `True`.
        strip_irrelevant_subdomains (bool, optional): Whether to strip irrelevant subdomains such as www etc.
            Default to True.
        strip_protocol (bool, optional): Whether to strip the url's protocol.
            Defaults to `True`.
        strip_fragment (bool|str, optional): Whether to drop non-routing fragment from the url?
            If set to `except-routing` will only drop non-routing fragment (i.e. fragments that
            do not contain a "/").
            Defaults to `except-routing`.
        normalize_amp (bool, optional): Whether to attempt to normalize Google
            AMP urls. Defaults to True.
        fix_common_mistakes (bool, optional): Whether to attempt solving common mistakes.
            Defaults to True.
        infer_redirection (bool, optional): Whether to attempt resolving common
            redirects by leveraging well-known GET parameters. Defaults to `False`.

    Returns:
        string: The normalized url.

    """
    original_url_arg = url

    if infer_redirection:
        url = resolve(url)

    url = CONTROL_CHARS_RE.sub("", url)
    url = url.strip()
    url = upper_quoted(url)

    has_protocol = PROTOCOL_RE.match(url)

    # Ensuring scheme so parsing works correctly
    if not has_protocol:
        url = "http://" + url

    # Platform-specific magic
    if platform_aware:
        if is_facebook_url(url):
            p = parse_facebook_url(url)

            if p is not None:
                url = p.url

        elif is_youtube_url(url):
            url = normalize_youtube_url(url)

    # Parsing
    try:
        splitted = urlsplit(url)
    except ValueError:
        return original_url_arg

    scheme, netloc, path, query, fragment = splitted
    user, password, hostname, port = (
        splitted.username,
        splitted.password,
        splitted.hostname,
        splitted.port,
    )

    # Fixing common mistakes
    if fix_common_mistakes and query:
        query = fix_common_query_mistakes(query)

    # Handling punycode
    if hostname:
        hostname = decode_punycode_hostname(hostname)

    # Dropping :80 & :443
    if port == 80 or port == 443:
        port = None

    # Normalizing the path
    if path:
        trailing_slash = False
        if path.endswith("/") and len(path) > 1:
            trailing_slash = True
        path = normpath(path)
        if trailing_slash and not strip_trailing_slash:
            path = path + "/"

    # Handling Google AMP suffixes
    if normalize_amp:
        path = AMP_SUFFIXES_RE.sub("", path)

    # Dropping index:
    if strip_index:
        segments = path.rsplit("/", 1)

        if len(segments) != 0:
            last_segment = segments[-1]
            filename, _ = splitext(last_segment)

            if filename == "index" or filename == "default":
                segments.pop()
                path = "/".join(segments)

    # Dropping irrelevant query items
    qsl = []

    if query:
        domain_filter = None

        if splitted.hostname:
            domain_filter = next(
                (
                    f
                    for d, f in PER_DOMAIN_QUERY_FILTERS
                    if splitted.hostname.endswith(d)
                ),
                None,
            )

        # TODO: what to do of empty query items vs. no valued
        # TODO: should be dedupe query items?
        qsl = [
            item
            for item in safe_qsl_iter(query)
            if not should_strip_query_item(
                item,
                normalize_amp=normalize_amp,
                query_item_filter=query_item_filter,
                domain_filter=domain_filter,
            )
        ]

        if sort_query:
            qsl = sorted(qsl, key=qsl_sort_key)

    # Dropping fragment if it's not routing
    if fragment and strip_fragment:
        if strip_fragment is True or not should_strip_fragment(fragment):
            fragment = ""

    # Always dropping trailing slash with empty query & fragment
    if path == "/" and not fragment and not query:
        path = ""

    # Dropping irrelevant subdomains
    if hostname and strip_irrelevant_subdomains:
        hostname = re.sub(
            IRRELEVANT_SUBDOMAIN_AMP_RE if normalize_amp else IRRELEVANT_SUBDOMAIN_RE,
            "",
            hostname,
        )

    # Dropping scheme
    if strip_protocol or not has_protocol:
        scheme = ""

    # Dropping authentication
    if strip_authentication:
        user = None
        password = None

    # Normalizing AMP subdomains
    if normalize_amp and hostname and hostname.startswith("amp-"):
        hostname = hostname[4:]

    # Dropping trailing slash
    if strip_trailing_slash and path.endswith("/"):
        path = path.rstrip("/")

    # Quoting
    if user:
        if quoted:
            user = safely_quote(user)
        else:
            user = safely_unquote_auth_item(user)

    if password:
        if quoted:
            password = safely_quote(password)
        else:
            password = safely_unquote_auth_item(password)

    if quoted:
        path = safely_quote(path)
    else:
        path = safely_unquote_path(path)

    if quoted:
        qsl = safely_quote_qsl(qsl)
    else:
        qsl = safely_unquote_qsl(qsl)

    query = safe_serialize_qsl(qsl)

    if quoted:
        fragment = safely_quote(fragment)
    else:
        fragment = safely_unquote_fragment(fragment)

    # Result
    netloc = unsplit_netloc(user, password, hostname, port)
    result = SplitResult(scheme, netloc.lower(), path, query, fragment)

    if not unsplit:
        return result

    # TODO: check if works with `unsplit=False`
    if strip_protocol or not has_protocol:
        result = urlunsplit(result)[2:]
    else:
        result = urlunsplit(result)

    return result
