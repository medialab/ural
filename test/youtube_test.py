# =============================================================================
# Ural Youtube Unit Tests
# =============================================================================
from ural.youtube import (
    YoutubeChannel,
    YoutubeShort,
    YoutubeUser,
    YoutubeVideo,
    extract_video_id_from_youtube_url,
    is_youtube_channel_id,
    is_youtube_url,
    is_youtube_video_id,
    normalize_youtube_url,
    parse_youtube_url,
)

IS_TESTS = [
    ("https://youtube.com", True),
    ("youtu.be/ugroiehfetef", True),
    ("http://www.lemonde.fr", False),
    ("http://www.youtube.com", True),
    ("http://youtube.je", False),
    ("au.youtube.com", True),
    ("https://youtube.googleapis.com/", True),
    ("youtubekids.com", True),
    ("yt.be", True),
]

IS_VIDEO_ID_TESTS = [("92HWiOdpY2s", True), ("92HWiOdpY", False)]

IS_CHANNEL_ID_TESTS = [
    ("UCv4Cecqpm3cOv7N5N9NkMsQ", True),
    ("UCS94J1s6-qc8v7btCdS2pNg", True),
    ("UCvlE5gTbOvjiolFlEm-c_Ow", True),
    ("UCCCPCZNChQdGa9EkATeye4g", True),
    ("test", False),
    ("france24", False),
    ("@France24", False),
]

PARSE_TESTS = [
    (
        "https://www.youtube.com/watch?v=92HWiOdpY2s",
        YoutubeVideo(id="92HWiOdpY2s", playlist=None),
        "https://www.youtube.com/watch?v=92HWiOdpY2s",
    ),
    (
        "https://www.youtube.com/watch?id=4526&v=92HWiOdpY2s",
        YoutubeVideo(id="92HWiOdpY2s", playlist=None),
        "https://www.youtube.com/watch?v=92HWiOdpY2s",
    ),
    (
        "http://www.youtube.com/user/ojimfrance",
        YoutubeUser(id=None, name="ojimfrance"),
        "https://www.youtube.com/user/ojimfrance",
    ),
    (
        "https://www.youtube.com/taranisnews",
        YoutubeChannel(id=None, name="taranisnews"),
        "https://www.youtube.com/taranisnews",
    ),
    ("https://www.youtube.com/watch", None, "https://www.youtube.com/watch"),
    (
        "http://www.youtube.com/v/j1i_l0OeeMc",
        YoutubeVideo(id="j1i_l0OeeMc", playlist=None),
        "https://www.youtube.com/watch?v=j1i_l0OeeMc",
    ),
    (
        "http://www.youtube.com/video/8CCuerpdwnw",
        YoutubeVideo(id="8CCuerpdwnw", playlist=None),
        "https://www.youtube.com/watch?v=8CCuerpdwnw",
    ),
    (
        "http://www.youtube.com/c/NadineMoranoOfficiel",
        YoutubeChannel(id=None, name="NadineMoranoOfficiel"),
        "https://www.youtube.com/NadineMoranoOfficiel",
    ),
    (
        "http://www.youtube.com/embed/sC4l-LvAH_c?autoplay=1",
        YoutubeVideo(id="sC4l-LvAH_c", playlist=None),
        "https://www.youtube.com/watch?v=sC4l-LvAH_c",
    ),
    (
        "http://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA",
        YoutubeChannel(id="UCWvUxN9LAjJ-sTc5JJ3gEyA", name=None),
        "https://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA",
    ),
    (
        "http://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA/videos",
        YoutubeChannel(id="UCWvUxN9LAjJ-sTc5JJ3gEyA", name=None),
        "https://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA",
    ),
    (
        "https://www.youtube.com/signin?app=desktop&action_handle_signin=true&hl=fr&next=%2Fwatch%3Fv%3DyEtmZKE5jhw&pli=1&auth=awfzXEmX9BuMCCEWwI2MBuBdDBNxbe9_9ApWQnC_LyUJrV06XI3J4TSMOYXwSrdMjoOw",
        YoutubeVideo(id="yEtmZKE5jhw", playlist=None),
        "https://www.youtube.com/watch?v=yEtmZKE5jhw",
    ),
    (
        "https://accounts.youtube.com/accounts/SetSID?list=OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY&ssdc=1&sidt=ALWU2ctpK5UgBHaSlYgNAS6kKr5K2ViktmHTEQ46AaVcyfB9Ae5jfhUmnJ5XuJTojZDXSFe3pvpYgPf2bpZ58EWKSst0QSJN20EyKnRRoHx9TF4k3xJ14%2F1VNso2ULDtZP1UwAtvqQ2gIYFo%2Bb6SGlmlnZBeBx1rJEDlJKmXbE5j1NiZfQp%2BLYGunuhjot9yZXOrzB2jq6O2CXEkEOw%2Bv23hWOXuUsUaXam2bZ4iRtEFt0EPkMK5rNysv%2FsVs%2F0LJtXTXIOaFGkaTJMbn28zC4VOO2dODGdm8UdGDrDHaI%2FHsiOrasfhK9O182PSjpLmYcLQObLVm9Ai&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26action_handle_signin%3Dtrue%26hl%3Dfr%26next%3D%252Fwatch%253Fv%253DyEtmZKE5jhw%26pli%3D1%26auth%3DawfzdXEmX9BuMCCEWwI2MBuBdDBNxbe9_9ApWQnC_LyUJrVN06XI3J4TSMOYXwSrdMjoOw",
        YoutubeVideo(
            id="yEtmZKE5jhw", playlist="OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY"
        ),
        "https://www.youtube.com/watch?v=yEtmZKE5jhw&list=OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY",
    ),
    (
        "https://www.youtube.com/PressecitronHD/",
        YoutubeChannel(id=None, name="PressecitronHD"),
        "https://www.youtube.com/PressecitronHD",
    ),
    (
        "http://www.youtube.com/profile_redirector/102339060754169863014",
        None,
        "http://www.youtube.com/profile_redirector/102339060754169863014",
    ),
    (
        "http://youtu.be/afa-5HQHiAs",
        YoutubeVideo(id="afa-5HQHiAs", playlist=None),
        "https://www.youtube.com/watch?v=afa-5HQHiAs",
    ),
    (
        "http://youtu.be/afa-5HQHiAs/",
        YoutubeVideo(id="afa-5HQHiAs", playlist=None),
        "https://www.youtube.com/watch?v=afa-5HQHiAs",
    ),
    (
        "http://youtu.be/4SpnqbXd8A8/video",
        YoutubeVideo(id="4SpnqbXd8A8", playlist=None),
        "https://www.youtube.com/watch?v=4SpnqbXd8A8",
    ),
    ("http://youtu.be/aHQHiAs", None, "http://youtu.be/aHQHiAs"),
    (
        "http://youtu.be/ZxCwPm_es4A?a",
        YoutubeVideo(id="ZxCwPm_es4A", playlist=None),
        "https://www.youtube.com/watch?v=ZxCwPm_es4A",
    ),
    (
        "https://youtu.be/rbXhnI_E0hQ%5D",
        YoutubeVideo(id="rbXhnI_E0hQ", playlist=None),
        "https://www.youtube.com/watch?v=rbXhnI_E0hQ",
    ),
    (
        "http://youtu.be/4SpnqbXd8A8%5B/video",
        YoutubeVideo(id="4SpnqbXd8A8", playlist=None),
        "https://www.youtube.com/watch?v=4SpnqbXd8A8",
    ),
    (
        "http://www.youtube.com/watch?v=3JqLhV80Vyg%20%20%28%20http%3A%2F%2Fyoutu.be%2F3JqLhV80Vyg%20%29",
        YoutubeVideo(id="3JqLhV80Vyg", playlist=None),
        "https://www.youtube.com/watch?v=3JqLhV80Vyg",
    ),
    (
        "https://m.youtube.com/?hl=fr&gl=FR#%2Fwatch%3Fv%3DObJTChxhhvY",
        YoutubeVideo(id="ObJTChxhhvY", playlist=None),
        "https://www.youtube.com/watch?v=ObJTChxhhvY",
    ),
    (
        "https://www.youtube.com/?hl=fr&gl=FR&app=desktop#/watch?v=ObJTChxhhvY",
        YoutubeVideo(id="ObJTChxhhvY", playlist=None),
        "https://www.youtube.com/watch?v=ObJTChxhhvY",
    ),
    (
        "http://www.youtube.com/v/mZiqexz7aqQ%26hl%3Den%26fs%3D1",
        YoutubeVideo(id="mZiqexz7aqQ", playlist=None),
        "https://www.youtube.com/watch?v=mZiqexz7aqQ",
    ),
    (
        "https://www.youtube.com/attribution_link?a=bWdZjuszr4I&u=%2Fwatch%3Fv%3Df5ZJLklAIQc%26feature%3Dshare",
        YoutubeVideo(id="f5ZJLklAIQc", playlist=None),
        "https://www.youtube.com/watch?v=f5ZJLklAIQc",
    ),
    (
        "https://www.youtube.com/results?search_query=Nicolas+Sarkozy+Amar+Saadani+Drs",
        None,
        "https://www.youtube.com/results?search_query=Nicolas+Sarkozy+Amar+Saadani+Drs",
    ),
    (
        "https://www.youtube.com/feed/history",
        None,
        "https://www.youtube.com/feed/history",
    ),
    ("https://youtube.com/channel/", None, "https://youtube.com/channel/"),
    (
        "https://youtube.com/c",
        YoutubeChannel(id=None, name="c"),
        "https://www.youtube.com/c",
    ),
    ("https://youtube.com/c/", None, "https://youtube.com/c/"),
    ("https://youtube.com/user/", None, "https://youtube.com/user/"),
    (
        "https://youtube.com/c/28minutes?cbrd=1&ucbcb=1",
        YoutubeChannel(id=None, name="28minutes"),
        "https://www.youtube.com/28minutes",
    ),
    (
        "https://youtube.com/channel/UCLIK2q7Y59uB_TXFjn2XdNg?cbrd=1&ucbcb=1",
        YoutubeChannel(id="UCLIK2q7Y59uB_TXFjn2XdNg", name=None),
        "https://www.youtube.com/channel/UCLIK2q7Y59uB_TXFjn2XdNg",
    ),
    (
        "https://youtube.com/watch?si=ELPmzJkLTLju2KnD5oyZMQ&v=Q5p-ZrwIC-0",
        YoutubeVideo(id="Q5p-ZrwIC-0", playlist=None),
        "https://www.youtube.com/watch?v=Q5p-ZrwIC-0",
    ),
    (
        "https://youtube.com/watch?ab_channel=matthieu&v=irmd-7xeocA",
        YoutubeVideo(id="irmd-7xeocA", playlist=None),
        "https://www.youtube.com/watch?v=irmd-7xeocA",
    ),
    (
        "https://youtube.com/watch?list=OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY&v=cTQjoHBhX4o",
        YoutubeVideo(
            id="cTQjoHBhX4o", playlist="OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY"
        ),
        "https://www.youtube.com/watch?v=cTQjoHBhX4o&list=OLAK5uy_k5D3LRPPwM7nIha78jFVoRU9RadBRsuPY",
    ),
    (
        "https://www.youtube.com/c/28minutesARTE",
        YoutubeChannel(id=None, name="28minutesARTE"),
        "https://www.youtube.com/28minutesARTE",
    ),
    (
        "https://www.youtube.com/28minutesARTE",
        YoutubeChannel(id=None, name="28minutesARTE"),
        "https://www.youtube.com/28minutesARTE",
    ),
    (
        "https://www.youtube.com/@28minutesARTE",
        YoutubeChannel(id=None, name="28minutesARTE"),
        "https://www.youtube.com/28minutesARTE",
    ),
    (
        "https://www.youtube.com/c/@28minutesARTE",
        YoutubeChannel(id=None, name="28minutesARTE"),
        "https://www.youtube.com/28minutesARTE",
    ),
    (
        "https://www.youtube.com/shorts/xnh-JKqktAU",
        YoutubeShort(id="xnh-JKqktAU"),
        "https://www.youtube.com/shorts/xnh-JKqktAU",
    ),
    (
        "https://www.youtube.com/shorts/U5Bn8mMxj4o/nonsense?whatever",
        YoutubeShort(id="U5Bn8mMxj4o"),
        "https://www.youtube.com/shorts/U5Bn8mMxj4o",
    ),
    (
        "https://www.youtube.com/shorts/",
        None,
        "https://www.youtube.com/shorts/",
    ),
]


class TestYoutube(object):
    def test_is_youtube_url(self):
        for url, result in IS_TESTS:
            assert is_youtube_url(url) == result

    def test_is_youtube_video_id(self):
        for v, result in IS_VIDEO_ID_TESTS:
            assert is_youtube_video_id(v) == result

    def test_is_youtube_channel_id(self):
        for v, result in IS_CHANNEL_ID_TESTS:
            assert is_youtube_channel_id(v) == result

    def test_parse_youtube_url(self):
        for url, result, _ in PARSE_TESTS:
            assert parse_youtube_url(url) == result

    def test_extract_video_id_from_youtube_url(self):
        for url, result, _ in PARSE_TESTS:
            extract_result = result.id if isinstance(result, YoutubeVideo) else None

            assert extract_video_id_from_youtube_url(url) == extract_result

    def test_normalize_youtube_url(self):
        for url, _, normalized in PARSE_TESTS:
            assert normalize_youtube_url(url) == normalized
