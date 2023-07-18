# -*- coding: utf-8 -*-
# =============================================================================
# Ural Quote Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural.quote import unquote, safely_unquote_auth


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
        assert unquote("%20", unsafe=(" ",)) == "%20"

        # assert unquote("%C3%A9%20", unsafe=(" ")) == "é%20"

        # assert safely_unquote_auth('t%C3%A9%40%3A') == "té%40%3A"
