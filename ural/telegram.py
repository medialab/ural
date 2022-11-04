# =============================================================================
# Ural Telegram-related heuristic functions
# =============================================================================
#
# Collection of functions related to Telegram urls.
#
import re
from collections import namedtuple

from ural.ensure_protocol import ensure_protocol
from ural.utils import urlpathsplit, urlsplit, urlunsplit, safe_urlsplit, SplitResult
from ural.patterns import DOMAIN_TEMPLATE

TELEGRAM_MESSAGE_ID_RE = re.compile(r"^\d+$")
TELEGRAM_DOMAINS_RE = re.compile(r"(?:telegram\.(?:org|me)|t\.me)$", re.I)
TELEGRAM_URL_RE = re.compile(
    DOMAIN_TEMPLATE % r"(?:[^.]+\.)*(?:telegram\.(?:org|me)|t\.me)", re.I
)
TELEGRAM_PUBLIC_REPLACE_RE = re.compile(
    r"^(?:[^.]+\.)?(?:telegram\.(?:org|me)|t\.me)", re.I
)

TelegramMessage = namedtuple("TelegramMessage", ["name", "id"])
TelegramGroup = namedtuple("TelegramGroup", ["id"])
TelegramChannel = namedtuple("TelegramChannel", ["name"])


def is_telegram_message_id(value):
    return bool(re.search(TELEGRAM_MESSAGE_ID_RE, value))


def is_telegram_url(url):
    """
    Function returning whether the given url is a valid Telegram url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Telegram.

    """
    if isinstance(url, SplitResult):
        return bool(re.search(TELEGRAM_DOMAINS_RE, url.hostname))

    return bool(re.match(TELEGRAM_URL_RE, url))


def convert_telegram_url_to_public(url):
    """
    Function parsing the given telegram url and returning the same but the
    the public version.
    """
    safe_url = ensure_protocol(url)

    has_protocol = safe_url == url

    scheme, netloc, path, query, fragment = urlsplit(safe_url)

    if not is_telegram_url(netloc):
        raise TypeError(
            "ural.telegram.convert_telegram_url_to_public: %s is not a telegram url"
            % url
        )

    netloc = re.sub(TELEGRAM_PUBLIC_REPLACE_RE, "t.me/s", netloc)

    result = (scheme, netloc, path, query, fragment)

    result = urlunsplit(result)

    if not has_protocol:
        result = result.split("://", 1)[-1]

    return result


def parse_telegram_url(url):
    """
    Function parsing the given url and returning either a TelegramMessage,
    TelegramChannel, TelegramGroup or None if nothing of information could be
    found.

    Args:
        url (str): Url to parse.

    """
    if not is_telegram_url(url):
        return None

    parsed = safe_urlsplit(url)
    path = urlpathsplit(parsed.path)

    if path:

        if path[0] == "s":

            if path[1] == "joinchat":
                if len(path) == 3:
                    return TelegramGroup(id=path[2])
                else:
                    None

            elif len(path) == 3 and is_telegram_message_id(path[2]):
                return TelegramMessage(name=path[1], id=path[2])

            elif len(path) == 2:
                return TelegramChannel(name=path[1])

            return None

        else:

            if path[0] == "joinchat":

                if len(path) == 3:
                    return TelegramGroup(id=path[2])

                elif len(path) == 2:
                    return TelegramGroup(id=path[1])

                else:
                    None

            elif len(path) == 2 and is_telegram_message_id(path[1]):
                return TelegramMessage(name=path[0], id=path[1])

            elif len(path) == 1:
                return TelegramChannel(name=path[0])

    return None


def extract_channel_name_from_telegram_url(url):
    parsed = parse_telegram_url(url)

    if parsed is None or isinstance(parsed, TelegramGroup):
        return

    return parsed.name
