# =============================================================================
# Ural Library Endpoint
# =============================================================================
#
from ural.classes.hostname_trie_set import HostnameTrieSet

from ural.could_be_html import could_be_html
from ural.ensure_protocol import ensure_protocol
from ural.force_protocol import force_protocol
from ural.get_hostname import get_hostname
from ural.infer_redirection import infer_redirection
from ural.is_shortened_url import is_shortened_url
from ural.is_typo_url import is_typo_url
from ural.is_url import is_url
from ural.normalize_url import (
    normalize_url,
    get_normalized_hostname,
    normalize_hostname,
)
from ural.should_follow_href import should_follow_href
from ural.should_resolve import should_resolve
from ural.strip_protocol import strip_protocol
from ural.tld import (
    get_domain_name,
    has_valid_suffix,
    split_suffix,
    is_valid_tld,
    has_valid_tld,
)
from ural.urls_from_text import urls_from_text
from ural.urls_from_html import urls_from_html
from ural.is_homepage import is_homepage
from ural.has_special_host import has_special_host, is_special_host
