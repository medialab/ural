from typing import Optional
from ural.types import AnyUrlTarget

def is_facebook_id(value: str) -> bool: ...
def is_facebook_full_id(value: str) -> bool: ...
def is_facebook_url(url: AnyUrlTarget) -> bool: ...
def is_facebook_post_url(url: AnyUrlTarget) -> bool: ...
def is_facebook_link(url: AnyUrlTarget) -> bool: ...
def extract_url_from_facebook_link(url: str) -> Optional[str]: ...
def convert_facebook_url_to_mobile(url: str) -> str: ...

class FacebookParsedItem(object):
    @property
    def url(self) -> str: ...

class FacebookUser(FacebookParsedItem):
    id: str
    handle: Optional[str]

    def __init__(self, id: str, handle=None): ...

class FacebookHandle(FacebookParsedItem):
    handle: str

    def __init__(self, handle: str): ...

class FacebookGroup(FacebookParsedItem):
    id: str
    handle: Optional[str]

    def __init__(self, id: str, handle=None): ...

class FacebookPost(FacebookParsedItem):
    id: str
    parent_id: Optional[str]
    parent_handle: Optional[str]
    group_id: Optional[str]
    group_handle: Optional[str]

    def __init__(
        self,
        post_id: str,
        parent_id: Optional[str] = None,
        parent_handle: Optional[str] = None,
        group_id: Optional[str] = None,
        group_handle: Optional[str] = None,
    ): ...
    @property
    def full_id(self) -> Optional[str]: ...

class FacebookVideo(FacebookParsedItem):
    id: str
    video_id: Optional[str]
    parent_id: Optional[str]

    def __init__(self, video_id: str, parent_id: Optional[str] = None): ...

class FacebookPhoto(FacebookParsedItem):
    id: str
    group_id: Optional[str]
    parent_id: Optional[str]
    parent_handle: Optional[str]
    album_id: Optional[str]

    def __init__(
        self,
        photo_id: str,
        group_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        parent_handle: Optional[str] = None,
        album_id: Optional[str] = None,
    ): ...

def parse_facebook_url(
    url: AnyUrlTarget, allow_relative_urls: bool = ...
) -> Optional[FacebookParsedItem]: ...
def has_facebook_comments(
    url: AnyUrlTarget, allow_relative_urls: bool = ...
) -> bool: ...
