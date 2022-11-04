# =============================================================================
# Ural Google-related heuristic functions
# =============================================================================
#
# Collection of functions related to Google urls.
#
import re
from ural.utils import safe_urlsplit, unquote, urlpathsplit
from ural.patterns import QUERY_VALUE_IN_URL_TEMPLATE

AMP_QUERY_RE = re.compile(r"amp(_.+)=?", re.I)
AMP_SUFFIXES_RE = re.compile(r"(?:\.amp(?=\.html$)|\.amp/?$|(?<=/)amp/?$)", re.I)

URL_EXTRACT_RE = re.compile(QUERY_VALUE_IN_URL_TEMPLATE % r"url")

DRIVE_TYPES = ["document", "presentation", "spreadsheets"]


def is_amp_url(url):
    splitted = safe_urlsplit(url)

    if splitted.hostname.endswith(".ampproject.org"):
        return True

    if splitted.hostname.startswith("amp-"):
        return True

    if splitted.hostname.startswith("amp."):
        return True

    if "/amp/" in splitted.path:
        return True

    if AMP_SUFFIXES_RE.search(splitted.path):
        return True

    if splitted.query and AMP_QUERY_RE.search(splitted.query):
        return True

    return False


def is_google_link(url):
    splitted = safe_urlsplit(url)

    if not splitted.hostname or "google." not in splitted.hostname:
        return False

    if splitted.path != "/url":
        return False

    return True


def extract_url_from_google_link(url):
    m = URL_EXTRACT_RE.search(url)

    if m is None:
        return None

    return unquote(m.group(1))


class GoogleDriveParsedItem(object):
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        for attr in self.__slots__:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __repr__(self):
        class_name = self.__class__.__name__

        representation = "<" + class_name

        for key in self.__slots__:
            value = getattr(self, key)

            if value is None:
                continue

            representation += " %s=%s" % (key, value)

        representation += ">"

        return representation


class GoogleDriveFile(GoogleDriveParsedItem):
    __slots__ = ("type", "id")

    def __init__(self, _type, _id):
        self.type = _type
        self.id = _id

    @property
    def url(self):
        return "https://docs.google.com/%s/d/%s" % (self.type, self.id)

    def get_export_url(self, format="csv"):
        return "https://docs.google.com/%s/d/%s/export?exportFormat=%s" % (
            self.type,
            self.id,
            format,
        )


class GoogleDrivePublicLink(GoogleDriveParsedItem):
    __slots__ = ("type", "id")

    def __init__(self, _type, _id):
        self.type = _type
        self.id = _id

    @property
    def url(self):
        return "https://docs.google.com/%s/d/e/%s/pub" % (self.type, self.id)

    def get_export_url(self, format="csv"):
        return "https://docs.google.com/%s/d/e/%s/pub?output=%s" % (
            self.type,
            self.id,
            format,
        )


def parse_google_drive_url(url):
    splitted = safe_urlsplit(url)

    if "docs.google.com" not in splitted.netloc:
        return None

    path = urlpathsplit(splitted.path)

    if len(path) < 3:
        return None

    drive_type = path[0]

    if drive_type not in DRIVE_TYPES:
        return None

    if path[1] != "d":
        return None

    if path[-1] == "pub":
        if path[2] != "e":
            return None

        return GoogleDrivePublicLink(drive_type, path[3])

    return GoogleDriveFile(drive_type, path[2])


def extract_id_from_google_drive_url(url):
    parsed = parse_google_drive_url(url)

    if isinstance(parsed, GoogleDriveFile):
        return parsed.id

    return None
