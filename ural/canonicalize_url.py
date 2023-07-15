from ural.utils import (
    urlsplit,
    urlunsplit,
    SplitResult,
    unsplit_netloc,
    space_aware_unquote,
    decode_punycode_hostname,
)
from ural.ensure_protocol import ensure_protocol
from ural.patterns import CONTROL_CHARS_RE


def canonicalize_url(url, default_protocol="https", unsplit=True):
    # Cleaning
    url = url.strip()
    url = CONTROL_CHARS_RE.sub("", url)

    # Ensuring a protocol
    url = ensure_protocol(url, default_protocol)

    # Parsing
    splitted = urlsplit(url)
    scheme, netloc, path, query, fragment = splitted
    user, password, hostname, port = (
        splitted.username,
        splitted.password,
        splitted.hostname,
        splitted.port,
    )

    # Decoding and normalizing hostname
    if hostname:
        hostname = decode_punycode_hostname(hostname)
        hostname = hostname.lower()

    # Dropping HTTP/HTTPS ports
    if port == "80" or port == "443":
        port = ""

    netloc = unsplit_netloc(user, password, hostname, port)

    # Unquoting
    path = space_aware_unquote(path)
    query = space_aware_unquote(query)
    fragment = space_aware_unquote(fragment)

    result = SplitResult(scheme, netloc, path, query, fragment)

    if not unsplit:
        return result

    # Serializing
    return urlunsplit(result)
