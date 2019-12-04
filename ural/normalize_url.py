# =============================================================================
# Ural URL Normalization Function
# =============================================================================
#
# A handy function relying on heuristics to find and drop irrelevant or
# non-discriminant parts of a URL.
#
import re
import pycountry
from os.path import normpath, splitext

from ural.ensure_protocol import ensure_protocol
from ural.utils import parse_qsl, urlsplit, urlunsplit, SplitResult
from ural.patterns import PROTOCOL_RE

IRRELEVANT_QUERY_PATTERN = r'^(?:__twitter_impression|echobox|fbclid|fref|utm_.+%s|s?een|xt(?:loc|ref|cr|np|or|s))$'
IRRELEVANT_SUBDOMAIN_PATTERN = r'\b(?:www\d?|mobile%s|m)\.'

AMP_QUERY_PATTERN = r'|amp_.+|amp'
AMP_SUBDOMAIN_PATTERN = r'|amp'
AMP_SUFFIXES_RE = re.compile(r'(?:\.amp(?=\.html$)|\.amp/?$|(?<=/)amp/?$)', re.I)
AMPPROJECT_REDIRECTION_RE = re.compile(r'^/[cv]/(?:s/)?', re.I)

IRRELEVANT_QUERY_RE = re.compile(IRRELEVANT_QUERY_PATTERN % r'', re.I)
IRRELEVANT_SUBDOMAIN_RE = re.compile(IRRELEVANT_SUBDOMAIN_PATTERN % r'', re.I)

IRRELEVANT_QUERY_AMP_RE = re.compile(IRRELEVANT_QUERY_PATTERN % AMP_QUERY_PATTERN, re.I)
IRRELEVANT_SUBDOMAIN_AMP_RE = re.compile(IRRELEVANT_SUBDOMAIN_PATTERN % AMP_SUBDOMAIN_PATTERN, re.I)

IRRELEVANT_QUERY_COMBOS = {
    'ref': ('fb', 'ts', 'tw', 'tw_i', 'twitter'),
    'spref': ('fb', 'ts', 'tw', 'tw_i', 'twitter'),
    'platform': ('hootsuite', )
}


def attempt_to_decode_idna(string):
    try:
        return string.encode('utf8').decode('idna')
    except:
        return string


def stringify_qs(item):
    if item[1] == '':
        return item[0]

    return '%s=%s' % item


def should_strip_query_item(item, normalize_amp=True):
    key = item[0].lower()

    pattern = IRRELEVANT_QUERY_AMP_RE if normalize_amp else IRRELEVANT_QUERY_RE

    if pattern.match(key):
        return True

    value = item[1]

    if key in IRRELEVANT_QUERY_COMBOS:
        return value in IRRELEVANT_QUERY_COMBOS[key]

    return False


# TODO: exclude #/ and #!/ raws
def is_routing_fragment(fragment):
    return (
        fragment.startswith('/') or
        fragment.startswith('!')
    )


def decode_punycode(netloc):
    if 'xn--' in netloc:
        netloc = '.'.join(
            attempt_to_decode_idna(x) for x in netloc.split('.')
        )

    return netloc


def strip_lang_subdomains_from_netloc(netloc):
    if netloc.count('.') > 1:
        subdomain, remaining_netloc = netloc.split('.', 1)
        if len(subdomain) == 5 and '-' in subdomain:
            lang, country = subdomain.split('-', 1)
            if len(lang) == 2 and len(country) == 2:
                if pycountry.countries.get(alpha_2=lang.upper()) and pycountry.countries.get(alpha_2=country.upper()):
                    netloc = remaining_netloc
        elif len(subdomain) == 2:
            if pycountry.countries.get(alpha_2=subdomain.upper()):
                netloc = remaining_netloc

    return netloc


def resolve_ampproject_redirect(splitted):
    if (
        splitted.hostname.endswith('.ampproject.org') and
        AMPPROJECT_REDIRECTION_RE.search(splitted.path)
    ):
        amp_redirected = 'https://' + AMPPROJECT_REDIRECTION_RE.sub('', splitted.path)

        if splitted.query:
            amp_redirected += '?' + splitted.query

        if splitted.fragment:
            amp_redirected += '#' + splitted.fragment

        splitted = urlsplit(amp_redirected)

    return splitted


def normalize_url(url, parsed=False, sort_query=True, strip_authentication=True,
                  strip_trailing_slash=False, strip_index=True, strip_protocol=True,
                  strip_irrelevant_subdomain=True, strip_lang_subdomains=False,
                  strip_fragment='except-routing', normalize_amp=True):
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
        strip_lang_subdomains (bool, optional): Whether to drop language subdomains
            (ex: 'fr-FR.lemonde.fr' to only 'lemonde.fr' because 'fr-FR' isn't a relevant subdomain, it indicates the language and the country).
            Defaults to `False`.
        strip_fragment (bool|str, optional): Whether to drop non-routing fragment from the url?
            If set to `except-routing` will only drop non-routing fragment (i.e. fragments that
            do not contain a "/").
            Defaults to `except-routing`.
        normalize_amp (bool, optional): Whether to attempt to normalize Google
            AMP urls. Defaults to True.

    Returns:
        string: The normalized url.

    """

    has_protocol = PROTOCOL_RE.match(url)

    # Ensuring scheme so parsing works correctly
    if not has_protocol:
        url = 'http://' + url

    # Parsing
    splitted = urlsplit(url)

    # Handling *.ampproject.org redirections
    if normalize_amp:
        splitted = resolve_ampproject_redirect(splitted)

    scheme, netloc, path, query, fragment = splitted

    # Handling punycode
    netloc = decode_punycode(netloc)

    # Dropping :80 & :443
    if netloc.endswith(':80'):
        netloc = netloc[:-3]
    elif netloc.endswith(':443'):
        netloc = netloc[:-4]

    # Normalizing the path
    if path:
        trailing_slash = False
        if path.endswith('/') and len(path) > 1:
            trailing_slash = True
        path = normpath(path)
        if trailing_slash and not strip_trailing_slash:
            path = path + '/'

    # Handling Google AMP suffixes
    if normalize_amp:
        path = AMP_SUFFIXES_RE.sub('', path)

    # Dropping index:
    if strip_index:
        segments = path.rsplit('/', 1)

        if len(segments) != 0:
            last_segment = segments[-1]
            filename, ext = splitext(last_segment)

            if filename == 'index':
                segments.pop()
                path = '/'.join(segments)

    # Dropping irrelevant query items
    if query:
        qsl = parse_qsl(query, keep_blank_values=True)
        qsl = [
            stringify_qs(item)
            for item in qsl
            if not should_strip_query_item(item, normalize_amp=normalize_amp)
        ]

        if sort_query:
            qsl = sorted(qsl)

        query = '&'.join(qsl)

    # Dropping fragment if it's not routing
    if fragment and strip_fragment:
        if strip_fragment is True or not is_routing_fragment(fragment):
            fragment = ''

    # Dropping irrelevant subdomains
    if strip_irrelevant_subdomain:
        netloc = re.sub(
            IRRELEVANT_SUBDOMAIN_AMP_RE if normalize_amp else IRRELEVANT_SUBDOMAIN_RE,
            '',
            netloc
        )

    # Dropping language as subdomains
    if strip_lang_subdomains:
        netloc = strip_lang_subdomains_from_netloc(netloc)

    # Dropping scheme
    if strip_protocol or not has_protocol:
        scheme = ''

    # Dropping authentication
    if strip_authentication:
        netloc = netloc.split('@', 1)[-1]

    # Normalizing AMP subdomains
    if normalize_amp and netloc.startswith('amp-'):
        netloc = netloc[4:]

    # Dropping trailing slash
    if strip_trailing_slash and path.endswith('/'):
        path = path.rstrip('/')

    # Result
    result = (
        scheme,
        netloc.lower(),
        path,
        query,
        fragment
    )

    if parsed:
        return result

    # TODO: check if works with `parsed=True`
    if strip_protocol or not has_protocol:
        result = urlunsplit(result)[2:]
    else:
        result = urlunsplit(result)

    return result


def get_normalized_hostname(url, normalize_amp=True, strip_lang_subdomains=False):
    if isinstance(url, SplitResult):
        splitted = url
    else:
        splitted = urlsplit(ensure_protocol(url))

    if normalize_amp:
        splitted = resolve_ampproject_redirect(splitted)

    hostname = splitted.hostname.lower()

    pattern = IRRELEVANT_SUBDOMAIN_AMP_RE if normalize_amp else IRRELEVANT_SUBDOMAIN_RE

    hostname = pattern.sub('', hostname)

    if normalize_amp and hostname.startswith('amp-'):
        hostname = hostname[4:]

    hostname = decode_punycode(hostname)

    if strip_lang_subdomains:
        hostname = strip_lang_subdomains_from_netloc(hostname)

    return hostname
