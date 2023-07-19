from ural.utils import (
    urlsplit,
    urlunsplit,
    SplitResult,
    unsplit_netloc,
    safe_qsl_iter,
    safe_serialize_qsl,
    decode_punycode_hostname,
    normpath,
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
from ural.ensure_protocol import ensure_protocol
from ural.patterns import CONTROL_CHARS_RE


def canonicalize_url(
    url, default_protocol="https", unsplit=True, quoted=False, strip_fragment=False
):
    # Cleaning
    url = CONTROL_CHARS_RE.sub("", url)
    url = url.strip()
    url = upper_quoted(url)

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
    if port == 80 or port == 443:
        port = None

    if strip_fragment:
        fragment = None

    # Empty path etc.
    if not path or path == "/":
        if not query and not fragment:
            path = ""
        else:
            path = "/"

    # Path normalization
    else:
        path = normpath(path)

    # Quotes
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

    qsl = safe_qsl_iter(query)

    if quoted:
        qsl = safely_quote_qsl(qsl)
    else:
        qsl = safely_unquote_qsl(qsl)

    query = safe_serialize_qsl(qsl)

    if fragment:
        if quoted:
            fragment = safely_quote(fragment)
        else:
            fragment = safely_unquote_fragment(fragment)

    # Repacking
    netloc = unsplit_netloc(user, password, hostname, port)
    result = SplitResult(scheme, netloc, path, query, fragment)

    if not unsplit:
        return result

    # Serializing
    return urlunsplit(result)
