from ural.is_shortened_url import SHORTENER_DOMAINS
from ural.hostname_trie_set import HostnameTrieSet

old_domains = set(SHORTENER_DOMAINS)

with open("./scripts/data/shortener-list.txt") as f:
    new_domains = set(d.strip() for d in f.readlines() if d.strip())

in_old_domains_only = old_domains - new_domains
in_new_domains_only = new_domains - old_domains

print()
print("Only in old domains:")
for d in in_old_domains_only:
    print("  -", d)

trie = HostnameTrieSet()

for d in old_domains:
    trie.add(d)

for d in new_domains:
    trie.add(d)

print()
print("Before", len(old_domains))
print("After", len(trie))

print(sorted(trie))
