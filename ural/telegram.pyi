from typing import NamedTuple, Union, Optional
from ural.types import AnyUrlTarget

def is_telegram_message_id(value: str) -> bool: ...
def is_telegram_url(url: AnyUrlTarget) -> bool: ...
def convert_telegram_url_to_public(url: str) -> Optional[str]: ...

class TelegramMessage(NamedTuple):
    name: str
    id: str

class TelegramGroup(NamedTuple):
    id: str

class TelegramChannel(NamedTuple):
    name: str

def parse_telegram_url(
    url: str,
) -> Optional[Union[TelegramMessage, TelegramGroup, TelegramChannel]]: ...
def extract_channel_name_from_telegram_url(url: str) -> Optional[str]: ...
