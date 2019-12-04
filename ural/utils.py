# =============================================================================
# Ural Various Utilities
# =============================================================================
#
# Miscellaneous utilities used throughout the library's code.
#

# PY2/PY3 compatible string_type...
string_type = str

try:
    string_type = basestring
except NameError:
    pass

# PY2/PY3 compatible urlparse
try:
    from urllib.parse import (
        parse_qs,
        parse_qsl,
        unquote,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult
    )
except ImportError:
    from urlparse import (
        parse_qs,
        parse_qsl,
        unquote,
        urljoin,
        urlsplit,
        urlunsplit,
        SplitResult
    )
