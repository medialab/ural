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
    ),
    (
        'https://www.youtube.com/signin?app=desktop&action_handle_signin=true&hl=fr&next=%2Fwatch%3Fv%3DyEtmZKE5jhw&pli=1&auth=awfzXEmX9BuMCCEWwI2MBuBdDBNxbe9_9ApWQnC_LyUJrV06XI3J4TSMOYXwSrdMjoOw',
        YoutubeVideo(id='yEtmZKE5jhw', user=None)
    ),
    (
        'https://accounts.youtube.com/accounts/SetSID?ssdc=1&sidt=ALWU2ctpK5UgBHaSlYgNAS6kKr5K2ViktmHTEQ46AaVcyfB9Ae5jfhUmnJ5XuJTojZDXSFe3pvpYgPf2bpZ58EWKSst0QSJN20EyKnRRoHx9TF4k3xJ14%2F1VNso2ULDtZP1UwAtvqQ2gIYFo%2Bb6SGlmlnZBeBx1rJEDlJKmXbE5j1NiZfQp%2BLYGunuhjot9yZXOrzB2jq6O2CXEkEOw%2Bv23hWOXuUsUaXam2bZ4iRtEFt0EPkMK5rNysv%2FsVs%2F0LJtXTXIOaFGkaTJMbn28zC4VOO2dODGdm8UdGDrDHaI%2FHsiOrasfhK9O182PSjpLmYcLQObLVm9Ai&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26action_handle_signin%3Dtrue%26hl%3Dfr%26next%3D%252Fwatch%253Fv%253DyEtmZKE5jhw%26pli%3D1%26auth%3DawfzdXEmX9BuMCCEWwI2MBuBdDBNxbe9_9ApWQnC_LyUJrVN06XI3J4TSMOYXwSrdMjoOw',
        YoutubeVideo(id='yEtmZKE5jhw', user=None)
    ),
    (
        'https://www.youtube.com/PressecitronHD/',
        YoutubeChannel(id=None, name='PressecitronHD')
    ),
    (
        'http://www.youtube.com/profile_redirector/102339060754169863014',
        YoutubeUser(id='102339060754169863014', name=None)
    )
]


class TestYoutube(object):
    def test_is_youtube_url(self):
        for url, result in IS_TESTS:
            assert is_youtube_url(url) == result

    def test_parse_youtube_url(self):
        for url, result in PARSE_TESTS:
            assert parse_youtube_url(url) == result
