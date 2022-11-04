#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Should Resolve Unit Tests
# =============================================================================
from ural import should_resolve
from test.is_shortened_test import TESTS

FULL_TESTS = TESTS + [("https://doi.org/10.4000/vertigo.26405", True)]


class TestShouldResolve(object):
    def test_basics(self):
        for url, result in TESTS:
            assert should_resolve(url) == result
