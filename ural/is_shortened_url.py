# =============================================================================
# Ural Shortened Url Testing Function
# =============================================================================
#
# Function testing whether the given url is probably a shortened url or not.
#
from ural.tries import HostnameTrieSet

SHORTENER_DOMAINS = [
    'adec.co',
    'amn.st',
    'bddy.me',
    'bit.ly',
    'bitly.com',
    'buff.ly',
    'crwd.fr',
    'disq.us',
    'dlvr.it',
    'ebx.sh',
    'ed.gr',
    'fal.cn',
    'fb.me',
    'feedproxy.google.com',
    'flip.it',
    'frama.link',
    'fw.to',
    'gerd.fm',
    'goo.gl',
    'go.shr.lc',
    'ht.ly',
    'hubs.ly',
    'ift.tt',
    'io.webhelp.com',
    'is.gd',
    'j.mp',
    'lc.cx',
    'lnkd.in',
    'loom.ly',
    'mon.actu.io',
    'msft.social',
    'mtr.cool',
    'non.li',
    'owl.li',
    'ow.ly',
    'po.st',
    'sco.lt',
    'shar.es',
    'soc.fm',
    'spr.ly',
    'swll.to',
    't.co',
    'tinyurl.com',
    'tmblr.co',
    'trib.al',
    'twib.in',
    'u.afp.com',
    'urlz.fr',
    'wp.me',
    'wrld.bg',
    'xfru.it',
    'youtu.be',
    'zpr.io'
]

# NOTE: we use a trie to perform efficient queries and so we don't
# need to test every domain/subdomain linearly
TRIE = HostnameTrieSet()

for domain in SHORTENER_DOMAINS:
    TRIE.add(domain)


def is_shortened_url(url):
    return TRIE.match(url)
