from ural.utils import (
    urlsplit,
    urlunsplit,
    SplitResult,
    unsplit_netloc,
    safe_qsl_iter,
    safe_serialize_qsl,
    decode_punycode_hostname,
)
from ural.quote import (
    safely_unquote_auth_item,
    safely_unquote_path,
    safely_unquote_qsl,
    safely_unquote_fragment,
    safely_quote,
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

    # Quotes
    if user:
        user = safely_unquote_auth_item(user)

    if password:
        password = safely_unquote_auth_item(password)

    path = safely_unquote_path(path)

    qsl = safely_unquote_qsl(safe_qsl_iter(query))
    query = safe_serialize_qsl(qsl)

    fragment = safely_unquote_fragment(fragment)

    # Repacking
    netloc = unsplit_netloc(user, password, hostname, port)
    result = SplitResult(scheme, netloc, path, query, fragment)

    if not unsplit:
        return result

    # Serializing
    return urlunsplit(result)
