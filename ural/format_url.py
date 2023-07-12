# -*- coding: utf-8 -*-
# =============================================================================
# Ural Format Url Function
# =============================================================================
#
# Function used to format urls conveniently.
#
from __future__ import unicode_literals

try:
    from collections.abc import Iterable
except ImportError:
    Iterable = (tuple, list, set, frozenset)

from ural.utils import string_type, quote


def format_query_argument(key, value, format_value=None):
    if format_value is not None:
        value = format_value(key, value)

    if value is True:
        return quote(key)

    return quote(key) + "=" + quote(str(value))


def format_url(
    base_url, path=None, args=None, format_arg_value=None, fragment=None, ext=None
):
    url = base_url

    # Path
    if isinstance(path, string_type):
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
    elif isinstance(path, Iterable):
        url = base_url.rstrip("/") + "/" + "/".join(path).lstrip("/")
    elif path is not None:
        raise TypeError("path should be a string or an iterable of path items")

    # Extension
    # NOTE: this can cause issues in some configurations, beware
    if ext is not None:
        url += "." + ext.lstrip(".")

    # Arguments
    if args is not None:
        items = sorted(
            (
                format_query_argument(k, v, format_arg_value)
                for k, v in args.items()
                if v is not None and v is not False
            )
        )

        if items:
            url += "?" + ("&".join(items))

    # Fragment
    if fragment is not None:
        url += "#" + fragment.lstrip("#")

    return url


class URLFormatter(object):
    BASE_URL = None

    def __init__(
        self,
        base_url=None,
        path=None,
        args=None,
        format_arg_value=None,
        fragment=None,
        ext=None,
    ):
        self.base_url = self.BASE_URL if base_url is None else base_url
        self.path = path
        self.args = args
        self._format_arg_value = format_arg_value
        self.fragment = fragment
        self.ext = ext

    def format_arg_value(self, k, v):
        return v

    def format(
        self,
        base_url=None,
        path=None,
        args=None,
        format_arg_value=None,
        fragment=None,
        ext=None,
    ):
        base_url = self.base_url if base_url is None else base_url
        path = self.path if path is None else path

        if format_arg_value is None:
            format_arg_value = self._format_arg_value

        if format_arg_value is None:
            format_arg_value = self.format_arg_value

        fragment = self.fragment if fragment is None else fragment

        # Args are merged
        if args is None:
            args = self.args
        else:
            if self.args is not None:
                new_args = self.args.copy()
                new_args.update(args)
                args = new_args

        return format_url(
            base_url=base_url,
            path=path,
            args=args,
            format_arg_value=format_arg_value,
            fragment=fragment,
            ext=ext,
        )

    def __call__(
        self,
        base_url=None,
        path=None,
        args=None,
        format_arg_value=None,
        fragment=None,
        ext=None,
    ):
        return self.format(
            base_url=base_url,
            path=path,
            args=args,
            format_arg_value=format_arg_value,
            fragment=fragment,
            ext=ext,
        )
