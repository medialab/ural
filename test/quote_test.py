# -*- coding: utf-8 -*-
# =============================================================================
# Ural Quote Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural.quote import (
    unquote,
    safely_unquote_auth,
    safely_unquote_path,
    safely_unquote_query_item,
    safely_quote,
)


class TestUnquote(object):
    def test_basics(self):
        assert unquote("test") == "test"
        assert unquote("t%C3%A9st") == "tést"
        assert unquote("tést") == "tést"
        assert unquote("té%C3%A9st") == "téést"
        assert unquote("%3T") == "%3T"

        assert unquote("%00") == "\x00"
        assert unquote("%00", only_printable=True) == "%00"

        assert unquote("%20") == " "
        assert unquote("%20", unsafe=(b" ",)) == "%20"

        assert unquote("%C3%A9%20", unsafe=(b" ")) == "é%20"

    def test_safe(self):
        assert safely_unquote_auth("t%C3%A9%40%3A%20") == "té%40%3A%20"
        assert safely_unquote_path("%C3%A9%3F%20") == "é%3F%20"
        assert safely_unquote_query_item("%C3%A9%3F%26%3D%20") == "é%3F%26%3D%20"
        assert safely_unquote_query_item("%C3%A9%3F%26%3D%20 ") == "é%3F%26%3D%20%20"


class TestQuote(object):
    def test_safe(self):
        assert safely_quote("té%20 ") == "t%C3%A9%20%20"
