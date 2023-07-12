from typing import NamedTuple, Union, Optional
from ural.types import AnyUrlTarget

class TwitterTweet(NamedTuple):
    user_screen_name: str
    id: str

class TwitterUser(NamedTuple):
    screen_name: str

class TwitterList(NamedTuple):
    id: str

def is_twitter_url(url: AnyUrlTarget) -> bool: ...
def normalize_screen_name(username: str) -> str: ...
def parse_twitter_url(
    url: AnyUrlTarget,
) -> Optional[Union[TwitterTweet, TwitterUser, TwitterList]]: ...
def extract_screen_name_from_twitter_url(url: AnyUrlTarget) -> Optional[str]: ...
