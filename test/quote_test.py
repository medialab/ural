# -*- coding: utf-8 -*-
# =============================================================================
# Ural Quote Unit Tests
# =============================================================================
from __future__ import unicode_literals

from ural.quote import unquote


class TestUnquote(object):
    def test_basics(self):
        assert unquote("test") == "test"
        assert unquote("t%C3%A9st") == "tést"
        assert unquote("%3T") == "%3T"

        assert unquote("%00") == "\x00"
        assert unquote("%00", only_printable=True) == "%00"
