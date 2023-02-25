from ural.utils import safe_urlsplit
from ural.has_special_host import is_special_host


class TLDTrieNode(object):
    __slots__ = ("children", "exception", "leaf", "private")

    def __init__(self):
        self.children = None
        self.exception = None
        self.leaf = False
        self.private = False


class TLDTrie(object):
    def __init__(self):
        self.__root = TLDTrieNode()

    def add(self, tld, private=False):
        node = self.__root

        # Iterating over the tld parts in reverse order
        for part in reversed(tld.split(".")):

            if part.startswith("!"):
                node.exception = part[1:]
                break

            # To save up some RAM, we initialize the children dict only
            # when strictly necessary
            if node.children is None:
                node.children = {}
                child = TLDTrieNode()
                node.children[part] = child
            else:
                child = node.children.get(part)
                if child is None:
                    child = TLDTrieNode()
                    node.children[part] = child

            node = child

        node.leaf = True

        if private:
            node.private = True

    def __match(self, url):
        parsed = safe_urlsplit(url)

        if is_special_host(parsed.hostname):
            return None

        hostname = parsed.hostname.lower().rstrip(".")
        parts = hostname.split(".")

        current_length = 0
        tld_length = 0
        match = None
        l = len(parts)

        node = self.__root

        for i in range(l - 1, -1, -1):
            part = parts[i]

            # Cannot go deeper
            if node.children is None:
                break

            # Exception
            if part == node.exception:
                break

            child = node.children.get(part)

            # Wildcards
            if child is None:
                child = node.children.get("*")

            # If the current part is not in current node's children, we can stop
            if child is None:
                break

            # Else we move deeper and increment our tld offset
            current_length += 1
            node = child

            if node.leaf:
                tld_length = current_length
                match = node

        # Checking the node we finished on is a leaf and is one we allow
        if match is None or not match.leaf:
            return None

        if l == tld_length:
            non_zero_i = -1  # hostname = tld
        else:
            non_zero_i = max(1, l - tld_length)

        return parts, non_zero_i, parsed
