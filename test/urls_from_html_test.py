#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Extraction From HTML Unit Tests
# =============================================================================
from ural import urls_from_html

HTML = """
<strong><span id="ref475087"></span>Ural Mountains</strong>, also called <strong>the Urals http://www.thisurlshouldnotmatch.com, </strong>Russian <strong>Uralskie Gory </strong>or <strong>Ural</strong>,  mountain range forming a rugged spine in west-central <span id="ref288737"></span><a href="https://www.britannica.com/place/Russia" class="md-crosslink">Russia</a> and the major part of the traditional physiographic boundary between <a href="https://www.britannica.com/place/Europe" class="md-crosslink">Europe</a> and <a href="https://www.britannica.com/place/Asia" class="md-crosslink">Asia</a>. Extending some 1,550 miles (2,500 km) from the bend of the <a href="https://www.britannica.com/place/Ural-River" class="md-crosslink">Ural River</a> in the south to the low, severely eroded <span id="ref288738"></span>Pay-Khoy Ridge, which forms a 250-mile (400-km) fingerlike extension to the northern tip of the Urals proper, the mountains <a href="https://www.merriam-webster.com/dictionary/constitute" class="md-dictionary-link" data-term="constitute">constitute</a> the major portion of the Uralian orogenic belt, which stretches 2,175 miles (3,500 km) from the <a href="https://www.britannica.com/place/Aral-Sea" class="md-crosslink">Aral Sea</a> to the northernmost tip of <span id="ref288739"></span><a href="https://www.britannica.com/place/Novaya-Zemlya" class="md-crosslink">Novaya Zemlya</a>.
"""

HTML_WITH_SCRIPT_TAGS = """
<div>
    <a href="http://lemonde.fr"></a>
    <script>
        console.log('<a href="http://bad.fr"></a>')
    </script>
</div>
<script type="text/javascript">
    console.log('<a href="http://bad.fr"></a>')
</script>
<script nomodule type="text/javascript">
    console.log('<a href="http://bad.fr"></a>')</script>
"""

REF_SET = set(
    [
        "https://www.britannica.com/place/Russia",
        "https://www.britannica.com/place/Europe",
        "https://www.britannica.com/place/Asia",
        "https://www.britannica.com/place/Ural-River",
        "https://www.merriam-webster.com/dictionary/constitute",
        "https://www.britannica.com/place/Aral-Sea",
        "https://www.britannica.com/place/Novaya-Zemlya",
    ]
)


class TestUrlsFromHtml(object):
    def test_basics(self):
        assert set(urls_from_html(HTML)) == REF_SET

    def test_edge_cases(self):
        assert list(urls_from_html('<a href="#">(415) 735-4488</a>')) == ["#"]
        assert list(urls_from_html('<a href="./test">(415) 735-4488</a>')) == ["./test"]
        assert list(urls_from_html("<a href=http://lemonde.fr></a>")) == [
            "http://lemonde.fr"
        ]
        assert list(urls_from_html("<a href=http://lemonde.fr>")) == [
            "http://lemonde.fr"
        ]
        assert list(urls_from_html("<a href='http://lemonde.fr'></a>")) == [
            "http://lemonde.fr"
        ]
        assert list(urls_from_html("<a \nhref='http://lemonde.fr'></a>")) == [
            "http://lemonde.fr"
        ]
        assert list(urls_from_html(HTML_WITH_SCRIPT_TAGS)) == ["http://lemonde.fr"]

    def test_binary(self):
        assert set(urls_from_html(HTML.encode())) == REF_SET
