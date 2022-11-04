from __future__ import unicode_literals
import re

PROTOCOL = r"[a-zA-Z]{0,64}:?//"
WEB_PROTOCOL = r"(?:(?:(?:https?|ftp|wss?):)?//)"
HTTP_PROTOCOL = r"https?://"

PROTOCOL_RE = re.compile(r"^%s" % PROTOCOL)
WEB_PROTOCOL_RE = re.compile(r"^%s" % WEB_PROTOCOL)
HTTP_PROTOCOL_RE = re.compile(r"^%s" % HTTP_PROTOCOL)

# Adapted from:
#  - https://gist.github.com/dperini/729294
#  - https://gist.github.com/pchc2005/b5f13e136a9c9bb2984e5b92802fc7c9
URL = (
    # protocol identifier
    # "(?:(?:(?:https?|ftp):)?//)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    # r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    # r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    # r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    r"localhost"
    r"|"
    # host & domain names, may end with dot
    # can be replaced by a shortest alternative
    # r"(?![-_])(?:[-\w\u00a1-\uffff]{0,63}[^-_]\.)+"
    # r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # # domain name
    # r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    r"(?:"
    r"(?:"
    r"[a-z0-9\u00a1-\uffff]"
    r"[a-z0-9\u00a1-\uffff_-]{0,62}"
    r")?"
    r"[a-z0-9\u00a1-\uffff]\."
    r")+"
    # TLD identifier name, may end with dot
    r"(?:[a-z\u00a1-\uffff]{2,}\.?)"
    r")"
    # port number (optional)
    r"(?::\d{2,5})?"
    # resource path (optional)
    # r"(?:[/?#]\S*)?"
)

RESOURCE_PATH = r"(?:[/?#]\S*)?"
RELAXED_RESOURCE_PATH = r"(?:[/?#][\S ]*)?"

SPECIAL_HOSTS_RE = re.compile(
    r"^localhost|(\d{1,3}\.){3}\d{1,3}|[\da-f]*:[\da-f:]*$", re.I
)

URL_RE = re.compile(r"^(?:%s)?%s$" % (PROTOCOL, URL + RESOURCE_PATH), re.I | re.UNICODE)

URL_WITH_PROTOCOL_RE = re.compile(
    r"^%s%s$" % (PROTOCOL, URL + RESOURCE_PATH), re.I | re.UNICODE
)

RELAXED_URL = re.compile(
    r"^(?:%s)?%s$" % (PROTOCOL, URL + RELAXED_RESOURCE_PATH), re.I | re.UNICODE
)

RELAXED_URL_WITH_PROTOCOL_RE = re.compile(
    r"^%s%s$" % (PROTOCOL, URL + RELAXED_RESOURCE_PATH), re.I | re.UNICODE
)

URL_IN_TEXT_RE = re.compile(
    r"(%s)%s" % (PROTOCOL, URL + RESOURCE_PATH), re.I | re.UNICODE
)

URL_IN_HTML_RE = re.compile(
    r"<a\s.*?href=(\S+?)(?:>|\s.*?>)(?:.*?)<[/ ]?a>", re.DOTALL | re.IGNORECASE
)

QUERY_VALUE_IN_URL_TEMPLATE = r"(?:^|[?&])%s=([^&]+)"
QUERY_VALUE_TEMPLATE = r"%s=([^&]+)"

DOMAIN_TEMPLATE = r"^(?:https?:)?(?://)?(?:\S+(?::\S*)?@)?%s(?:[:/#]|\s*$)"
