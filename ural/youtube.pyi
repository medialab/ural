from typing import NamedTuple, Optional, Union
from ural.types import AnyUrlTarget

class YoutubeVideo(NamedTuple):
    id: str

class YoutubeUser(NamedTuple):
    id: str
    name: str

class YoutubeChannel(NamedTuple):
    id: str
    name: str

def is_youtube_url(url: AnyUrlTarget) -> bool: ...
def is_youtube_video_id(value: str) -> bool: ...
def parse_youtube_url(
    url: AnyUrlTarget, fix_common_mistakes: bool = ...
) -> Optional[Union[YoutubeVideo, YoutubeUser, YoutubeChannel]]: ...
def extract_video_id_from_youtube_url(url: AnyUrlTarget) -> Optional[str]: ...
def normalize_youtube_url(url: AnyUrlTarget) -> str: ...
