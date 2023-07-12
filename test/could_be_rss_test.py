from ural.could_be_rss import could_be_rss

TESTS = [
    (
        "https://bienpublic.com/politique/2022/12/22/sncf-emmanuel-macron-rattrape-par-le-socialdlvr.it/SfK3Hp",
        False,
    ),
    (
        "https://lequipe.fr/Cyclisme-sur-route/Article/Dans-la-ferme-d-arnaud-de-lie-la-nouvelle-star-du-cyclisme-belge/1371577",
        False,
    ),
    ("https://wikiart.org/en/edward-hopper/not_detected_235603", False),
    (
        "https://play.google.com/store/apps/details?gl=US&hl=fr&id=com.bluetoothscannersc123c4e4e913r1z350999386162e5199.s3.amazonaws.com/web123w9b6n646d6w35099947387d007c9123p470ex620e555baaa745f37ecb6_fr.html",
        False,
    ),
    (
        "https://clermont.snes.edu/Acces-au-corps-des-agreges-par-liste-d-aptitude.htmlbit.ly/3UhuVXS",
        False,
    ),
    ("https://trib.al/gc5KIo5", False),
    ("https://rougememoire.com/article/quizsrfc-edition-journee-des-abonnes", False),
    (
        "https://changera3.blogspot.com/2022/12/charles-sannat-la-france-en-urgence.html",
        False,
    ),
    (
        "https://apnews.com/article/entertainment-richmond-6c847bb2e6e52a7048d44d2aacc2ef85?taid=63974840c89e5500011f71e0",
        False,
    ),
    ("https://legifrance.gouv.fr/jorf/texte_jo/JORFTEXT000046652536", False),
    #
    ("https://www.htmhell.dev/feed.xml", True),
    ("http://feeds.feedburner.com/2ality?format=xml", True),
    ("http://webkit.org/blog/feed/", True),
    ("http://blog.portswigger.net/feeds/posts/default", True),
    ("https://sindresorhus.com/rss.xml", True),
    ("https://blog.firsov.net/feeds/posts/default?alt=rss", True),
    ("http://jakearchibald.com/posts.rss", True),
    ("https://www.debugbear.com/blog/feed/rss", True),
    ("https://marcysutton.com/rss.xml", True),
    ("http://feeds.feedburner.com/kizuruen", True),
    #
    ("https://feeds.feedburner.com/TechCrunch/", True),
    ("https://feeds2.feedburner.com/TechCrunch/", True),
    (
        "https://linkedin.com/feed/update/urn%253Ali%253Aactivity%253A7013073227979608064",
        False,
    ),
    (
        "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
        True,
    ),
    ("https://news.google.com/__i/rss/rd/articles/CBMilwFodHRwczovL3d3dy", False),
    ("https://machin.com/feed/rss.html", False),
    ("https://machin.com/feed/", True),
]


class TestCouldBeRss(object):
    def test_basics(self):
        for url, test in TESTS:
            assert could_be_rss(url) == test
