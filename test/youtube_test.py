# =============================================================================
# Ural Youtube Unit Tests
# =============================================================================
import pytest
from ural.youtube import (
    is_youtube_url,
    parse_youtube_url,
    YoutubeVideo,
    YoutubeUser,
    YoutubeChannel
)

IS_TESTS = [
    ('https://youtube.com', True),
    ('youtu.be/ugroiehfetef', True),
    ('http://www.lemonde.fr', False)
]

PARSE_TESTS = [
    (
        'https://www.youtube.com/watch?v=92HWiOdpY2s',
        YoutubeVideo(id='92HWiOdpY2s', user=None)
    ),
    (
        'https://www.youtube.com/watch?id=4526&v=92HWiOdpY2s',
        YoutubeVideo(id='92HWiOdpY2s', user=None)
    ),
    (
        'http://www.youtube.com/user/ojimfrance',
        YoutubeUser(id=None, name='ojimfrance')
    ),
    (
        'https://www.youtube.com/taranisnews',
        YoutubeChannel(id=None, name='taranisnews')
    ),
    (
        'https://www.youtube.com/watch',
        None
    ),
    (
        'http://www.youtube.com/v/j1i_l0OeeMc',
        YoutubeVideo(id='j1i_l0OeeMc', user=None)
    ),
    (
        'http://www.youtube.com/video/8CCuerpdwnw',
        YoutubeVideo(id='8CCuerpdwnw', user=None)
    ),
    (
        'http://www.youtube.com/c/NadineMoranoOfficiel',
        YoutubeChannel(id=None, name='NadineMoranoOfficiel')
    ),
    (
        'http://www.youtube.com/embed/sC4l-LvAH_c?autoplay=1',
        YoutubeVideo(id='sC4l-LvAH_c', user=None)
    ),
    (
        'http://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA',
        YoutubeChannel(id='UCWvUxN9LAjJ-sTc5JJ3gEyA', name=None)
    ),
    (
        'http://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA/videos',
        YoutubeChannel(id='UCWvUxN9LAjJ-sTc5JJ3gEyA', name=None)
    )
]


class TestYoutube(object):
    def test_is_youtube_url(self):
        for url, result in IS_TESTS:
            assert is_youtube_url(url) == result

    def test_parse_youtube_url(self):
        for url, result in PARSE_TESTS:
            assert parse_youtube_url(url) == result
