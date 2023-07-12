import sys
from typing import Union, Optional
from urllib.parse import SplitResult

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

AnyUrlTarget = Union[str, SplitResult]
QueryArgValue = Optional[Union[str, int, float, bool]]
