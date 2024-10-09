from typing import Optional
from ural.types import AnyUrlTarget

def is_reddit_url(url: str) -> bool : ...
def is_subreddit_url(url: str) -> bool : ...
def is_reddit_user_url(url: str) -> bool : ...
def is_reddit_post_url(url: str) -> bool : ...
def convert_reddit_url_to_old_url(url: str) -> str : ...
def convert_old_reddit_url_to_new_url(url: str) -> str : ...