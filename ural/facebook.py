# =============================================================================
# Ural Facebook-related heuristic functions
# =============================================================================
#
# Collection of functions crafted to work with Facebook's urls.
#
import re

from ural.ensure_protocol import ensure_protocol
from ural.patterns import DOMAIN_TEMPLATE, QUERY_VALUE_IN_URL_TEMPLATE

from ural.utils import (
    safe_parse_qs,
    unquote,
    urljoin,
    urlpathsplit,
    urlsplit,
    urlunsplit,
    safe_urlsplit,
    SplitResult,
)

NUMERIC_ID_RE = re.compile(r"[0-9]{8,}")

BASE_FACEBOOK_URL = "https://www.facebook.com"

FACEBOOK_ID_RE = re.compile(r"^\d+$")
FACEBOOK_FULL_ID_RE = re.compile(r"^\d+_\d+$")
FACEBOOK_DOMAIN_RE = re.compile(r"(?:facebook\.[^.]+$|fb\.me$)", re.I)
FACEBOOK_URL_RE = re.compile(
    DOMAIN_TEMPLATE % r"(?:[^.]+\.)*(?:facebook\.[^.]+|fb\.me)", re.I
)
MOBILE_REPLACE_RE = re.compile(r"^([^.]+\.)?facebook\.", re.I)

URL_EXTRACT_RE = re.compile(QUERY_VALUE_IN_URL_TEMPLATE % r"u")


def is_facebook_id(value):
    return bool(re.search(FACEBOOK_ID_RE, value))


def is_facebook_full_id(value):
    return bool(re.search(FACEBOOK_FULL_ID_RE, value))


def is_facebook_url(url):
    """
    Function returning whether the given url is a valid Facebook url.

    Args:
        url (str): Url to test.

    Returns:
        bool: Whether given url is from Facebook.

    """
    if isinstance(url, SplitResult):
        return bool(re.search(FACEBOOK_DOMAIN_RE, url.hostname))

    return bool(re.match(FACEBOOK_URL_RE, url))


def is_facebook_post_url(url):
    if not is_facebook_url(url):
        return False

    return (
        "/posts/" in url
        or "/permalink/" in url
        or ("/permalink.php" in url and ("&id=" in url or "&amp;id=" in url))
        or ("/story.php" in url and ("&id=" in url or "&amp;id=" in url))
    )


def is_facebook_link(url):
    splitted = safe_urlsplit(url)

    if not splitted.hostname or ".facebook." not in splitted.hostname:
        return False

    if splitted.path != "/l.php":
        return False

    return True


def extract_url_from_facebook_link(url):
    m = URL_EXTRACT_RE.search(url)

    if m is None:
        return None

    return unquote(m.group(1))


def convert_facebook_url_to_mobile(url):
    """
    Function parsing the given facebook url and returning the same but for
    the mobile website.
    """
    safe_url = ensure_protocol(url)

    has_protocol = safe_url == url

    scheme, netloc, path, query, fragment = urlsplit(safe_url)

    if "facebook" not in netloc:
        raise TypeError(
            "ural.facebook.convert_facebook_url_to_mobile: %s is not a facebook url"
            % url
        )

    netloc = re.sub(MOBILE_REPLACE_RE, "m.facebook.", netloc)

    result = (scheme, netloc, path, query, fragment)

    result = urlunsplit(result)

    if not has_protocol:
        result = result.split("://", 1)[-1]

    return result


class FacebookParsedItem(object):
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


class FacebookUser(FacebookParsedItem):
    __slots__ = ("id", "handle")

    def __init__(self, id, handle=None):
        self.id = id
        self.handle = handle

    @property
    def url(self):
        if self.handle is None:
            return urljoin(BASE_FACEBOOK_URL, "/profile.php?id=%s" % self.id)

        return urljoin(BASE_FACEBOOK_URL, "/%s" % self.handle)


class FacebookHandle(FacebookParsedItem):
    __slots__ = ("handle",)

    def __init__(self, handle):
        self.handle = handle

    @property
    def url(self):
        return urljoin(BASE_FACEBOOK_URL, "/%s" % self.handle)


class FacebookGroup(FacebookParsedItem):
    __slots__ = ("id", "handle")

    def __init__(self, id=None, handle=None):
        self.id = id
        self.handle = handle

    @property
    def url(self):
        if self.handle is not None:
            return urljoin(BASE_FACEBOOK_URL, "groups/%s" % self.handle)

        return urljoin(BASE_FACEBOOK_URL, "groups/%s" % self.id)


class FacebookPost(FacebookParsedItem):
    __slots__ = ("id", "parent_id", "parent_handle", "group_id", "group_handle")

    def __init__(
        self,
        post_id,
        parent_id=None,
        parent_handle=None,
        group_id=None,
        group_handle=None,
    ):
        self.id = post_id
        self.parent_id = parent_id
        self.parent_handle = parent_handle
        self.group_id = group_id
        self.group_handle = group_handle

    @property
    def url(self):
        if self.parent_handle is not None:
            return urljoin(
                BASE_FACEBOOK_URL, "/%s/posts/%s" % (self.parent_handle, self.id)
            )

        if self.parent_id is not None:
            return urljoin(
                BASE_FACEBOOK_URL,
                "/permalink.php?story_fbid=%s&id=%s" % (self.id, self.parent_id),
            )

        if self.group_id is not None:
            return urljoin(
                BASE_FACEBOOK_URL, "/groups/%s/permalink/%s" % (self.group_id, self.id)
            )

        if self.group_handle is not None:
            return urljoin(
                BASE_FACEBOOK_URL,
                "/groups/%s/permalink/%s" % (self.group_handle, self.id),
            )

    @property
    def full_id(self):
        if self.parent_id is not None:
            return "%s_%s" % (self.parent_id, self.id)

        if self.group_id is not None:
            return "%s_%s" % (self.group_id, self.id)

        return None


class FacebookVideo(FacebookParsedItem):
    __slots__ = ("id", "parent_id")

    def __init__(self, video_id, parent_id=None):
        self.id = video_id
        self.parent_id = parent_id

    @property
    def url(self):
        if self.parent_id is None:
            return urljoin(BASE_FACEBOOK_URL, "/watch/?v=%s" % self.id)

        return urljoin(BASE_FACEBOOK_URL, "/%s/videos/%s" % (self.parent_id, self.id))


class FacebookPhoto(FacebookParsedItem):
    __slots__ = ("id", "group_id", "parent_id", "parent_handle", "album_id")

    def __init__(
        self, photo_id, group_id=None, parent_id=None, parent_handle=None, album_id=None
    ):
        self.id = photo_id
        self.group_id = group_id
        self.parent_id = parent_id
        self.parent_handle = parent_handle
        self.album_id = album_id

    @property
    def url(self):
        if self.group_id:
            return urljoin(
                BASE_FACEBOOK_URL,
                "/photo.php?fbid=%s&set=g.%s" % (self.id, self.group_id),
            )

        if self.parent_id:
            return urljoin(
                BASE_FACEBOOK_URL,
                "/%s/a.%s/%s" % (self.parent_id, self.album_id, self.id),
            )

        if self.parent_handle:
            return urljoin(
                BASE_FACEBOOK_URL,
                "/%s/a.%s/%s" % (self.parent_handle, self.album_id, self.id),
            )

        return urljoin(BASE_FACEBOOK_URL, "/photo.php?fbid=%s" % self.id)


def parse_facebook_url(url, allow_relative_urls=False):

    # Allowing relative urls scraped from facebook?
    if (
        allow_relative_urls
        and not url.startswith("http://")
        and not url.startswith("https://")
        and "facebook." not in url
    ):
        url = urljoin(BASE_FACEBOOK_URL, url)
    else:
        if not is_facebook_url(url):
            return None

    splitted = safe_urlsplit(url)

    if not splitted.path or splitted.path == "/":
        return None

    # Videos
    if "/watch" in splitted.path:
        query = safe_parse_qs(splitted.query)

        if "v" not in query:
            return None

        video_id = query["v"][0]

        return FacebookVideo(video_id)

    if "/videos/" in splitted.path:
        parts = urlpathsplit(splitted.path)

        return FacebookVideo(parts[2], parent_id=parts[0])

    # Photos
    if splitted.query and (
        splitted.path.endswith("/photo.php")
        or splitted.path.rstrip("/").endswith("/photo")
    ):
        query = safe_parse_qs(splitted.query)

        if "fbid" not in query:
            return None

        group_id = None
        album_id = None

        if "set" in query:
            sets = query["set"]

            group_id = next((s for s in sets if s.startswith("g.")), None)

            if group_id:
                group_id = group_id.split("g.", 1)[1]

            album_id = next((s for s in sets if s.startswith("a.")), None)

            if album_id:
                album_id = album_id.split("a.", 1)[1]

        return FacebookPhoto(query["fbid"][0], group_id=group_id, album_id=album_id)

    if "/photos/" in splitted.path:
        parts = urlpathsplit(splitted.path)

        parent_id_or_handle = parts[0]
        album_id = parts[2].replace("a.", "")
        photo_id = parts[3]

        if is_facebook_id(parent_id_or_handle):
            return FacebookPhoto(
                photo_id, album_id=album_id, parent_id=parent_id_or_handle
            )

        return FacebookPhoto(
            photo_id, album_id=album_id, parent_handle=parent_id_or_handle
        )

    # Obvious post path
    if "/posts/" in splitted.path:
        parts = urlpathsplit(splitted.path)

        if parts[0] == "groups":
            group_id_or_handle = parts[1]

            if NUMERIC_ID_RE.match(group_id_or_handle):
                return FacebookPost(parts[3], group_id=group_id_or_handle)
            return FacebookPost(parts[3], group_handle=group_id_or_handle)

        parent_id_or_handle = parts[0]

        if NUMERIC_ID_RE.match(parent_id_or_handle):
            return FacebookPost(parts[2], parent_id=parent_id_or_handle)

        return FacebookPost(parts[2], parent_handle=parent_id_or_handle)

    # Ye olded permalink path
    if splitted.query and (
        "/permalink.php" in splitted.path or "/story.php" in splitted.path
    ):
        query = safe_parse_qs(splitted.query)
        parent_id = query.get("id", None)

        if not parent_id:
            return None

        return FacebookPost(query["story_fbid"][0], parent_id=parent_id[0])

    # Group permalink path
    if "/groups/" in splitted.path:
        parts = urlpathsplit(splitted.path)

        if "/permalink/" in splitted.path:
            if is_facebook_id(parts[1]):
                return FacebookPost(parts[3], group_id=parts[1])

            return FacebookPost(parts[3], group_handle=parts[1])

        if is_facebook_id(parts[1]):
            return FacebookGroup(id=parts[1])

        return FacebookGroup(handle=parts[1])

    # Profile path
    if splitted.path == "/profile.php":
        query = safe_parse_qs(splitted.query)
        user_id = query["id"][0]
        return FacebookUser(user_id)

    # People path
    if splitted.path.startswith("/people"):
        parts = urlpathsplit(splitted.path)
        user_id = parts[2]
        return FacebookUser(user_id)

    # Handle path
    if splitted.path:
        parts = urlpathsplit(splitted.path)

        if not parts[0].endswith(".php"):
            return FacebookHandle(parts[0])

    return None


FACEBOOK_TYPES_HAVING_COMMENTS = (FacebookPost, FacebookPhoto, FacebookVideo)


def has_facebook_comments(url, allow_relative_urls=False):
    if not is_facebook_url(url):
        return False

    result = parse_facebook_url(url, allow_relative_urls=allow_relative_urls)

    return isinstance(result, FACEBOOK_TYPES_HAVING_COMMENTS)
