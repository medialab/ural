#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Ural Format Url Unit Tests
# =============================================================================
from ural.format_url import format_url, URLFormatter


class TestFormatUrl(object):
    def test_basics(self):
        assert format_url("http://lemonde.fr") == "http://lemonde.fr"
        assert format_url("http://lemonde.fr", path="/test") == "http://lemonde.fr/test"
        assert format_url("http://lemonde.fr", path="test") == "http://lemonde.fr/test"
        assert (
            format_url("http://lemonde.fr/", path="/test") == "http://lemonde.fr/test"
        )
        assert (
            format_url("http://lemonde.fr", fragment="test") == "http://lemonde.fr#test"
        )
        assert (
            format_url("http://lemonde.fr/test", path="second")
            == "http://lemonde.fr/test/second"
        )
        assert (
            format_url("http://lemonde.fr/test/", path="second")
            == "http://lemonde.fr/test/second"
        )
        assert (
            format_url("http://lemonde.fr/test", path="/second")
            == "http://lemonde.fr/test/second"
        )
        assert (
            format_url("http://lemonde.fr/test/", path="/second")
            == "http://lemonde.fr/test/second"
        )
        assert (
            format_url("http://lemonde.fr", fragment="#test")
            == "http://lemonde.fr#test"
        )
        assert (
            format_url("http://lemonde.fr", path="article", ext="html")
            == "http://lemonde.fr/article.html"
        )
        assert (
            format_url("http://lemonde.fr", path="article", ext=".html")
            == "http://lemonde.fr/article.html"
        )

        assert (
            (
                format_url(
                    "http://lemonde.fr",
                    path=["business", "articles"],
                    args={
                        "hello": "world",
                        "number": 14,
                        "boolean": True,
                        "skipped": None,
                        "also-skipped": False,
                        "quoted": "test=ok",
                        "k quoted": True,
                    },
                    fragment="#test",
                )
            )
            == "http://lemonde.fr/business/articles?boolean&hello=world&k%20quoted&number=14&quoted=test%3Dok#test"
        )

        def format_arg_value(k, v):
            if k == "ids":
                return ",".join(v)

            return v

        assert (
            format_url(
                "http://lemonde.fr",
                args={"id": "1", "ids": ["one", "two"]},
                format_arg_value=format_arg_value,
            )
            == "http://lemonde.fr?id=1&ids=one%2Ctwo"
        )

        assert (
            format_url("http://lemonde.fr", ["articles", 0, "article.html"])
            == "http://lemonde.fr/articles/0/article.html"
        )

    def test_formatter(self):
        formatter = URLFormatter("http://lemonde.fr")

        assert formatter() == "http://lemonde.fr"
        assert (
            formatter(path="/test", args={"two": 2}) == "http://lemonde.fr/test?two=2"
        )

        formatter = URLFormatter("http://lemonde.fr", args={"one": "1"})

        assert formatter() == "http://lemonde.fr?one=1"
        assert formatter(args={"one": 4}) == "http://lemonde.fr?one=4"
        assert formatter(args={"two": 2}) == "http://lemonde.fr?one=1&two=2"

        class LeMondeURLFormatter(URLFormatter):
            BASE_URL = "http://lemonde.fr"

            def format_arg_value(self, k, v):
                if k == "ids":
                    return ",".join(str(i) for i in v)

                return v

            def format_api_call(self, token):
                return self.format(args={"token": token})

            def format_with_list(self, ids):
                return self.format(args={"ids": ids})

            def format_with_list_overriden(self):
                return self.format(args={"ids": 45}, format_arg_value=lambda k, v: "no")

        formatter = LeMondeURLFormatter()

        assert formatter.format_api_call("yoyo") == "http://lemonde.fr?token=yoyo"
        assert formatter.format_with_list([1, 2]) == "http://lemonde.fr?ids=1%2C2"
        assert formatter.format_with_list_overriden() == "http://lemonde.fr?ids=no"
