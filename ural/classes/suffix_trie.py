from ural.utils import safe_urlsplit
from ural.has_special_host import is_special_host


class SuffixTrieNode(object):
    __slots__ = ("children", "exception", "leaf", "private")

    def __init__(self):
        self.children = None
        self.exception = None
        self.leaf = False
        self.private = False


class SuffixTrie(object):
    def __init__(self):
        self.__root = SuffixTrieNode()

    def add(self, suffix, private=False):
        node = self.__root

        # Iterating over the suffix parts in reverse order
        for part in reversed(suffix.split(".")):

            if part.startswith("!"):
                node.exception = part[1:]
                break

            # To save up some RAM, we initialize the children dict only
            # when strictly necessary
            if node.children is None:
                node.children = {}
                child = SuffixTrieNode()
                node.children[part] = child
            else:
                child = node.children.get(part)
                if child is None:
                    child = SuffixTrieNode()
                    node.children[part] = child

            node = child

        node.leaf = True

        if private:
            node.private = True

    def __walk(self, url):
        parsed = safe_urlsplit(url)

        if is_special_host(parsed.hostname):
            return None

        hostname = parsed.hostname.lower().rstrip(".")
        parts = hostname.split(".")

        current_length = 0
        suffix_length = 0
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

            # Else we move deeper and increment our suffix offset
            current_length += 1
            node = child

            if node.leaf:
                suffix_length = current_length
                match = node

        # Checking the node we finished on is a leaf and is one we allow
        if match is None or not match.leaf:
            return None

        # hostname = suffix ?
        if l == suffix_length:
            offset = -1
        else:
            offset = max(1, l - suffix_length)

        return match, parts, offset

    def split(self, url):
        result = self.__walk(url)

        if result is None:
            return None

        _, parts, offset = result

        # hostname = suffix
        if offset < 0:
            return "", ".".join(parts)

        return ".".join(parts[:offset]), ".".join(parts[offset:])

    def has_valid_domain_name(self, url):
        result = self.__walk(url)

        if result is None:
            return False

        return True

    def extract_suffix(self, url):
        result = self.__walk(url)

        if result is None:
            return None

        # TODO: we can restrict to public or private here easily
        _, parts, offset = result

        # hostname = suffix
        if offset < 0:
            return ".".join(parts)

        return ".".join(parts[offset:])

    def extract_domain_name(self, url):
        result = self.__walk(url)

        if result is None:
            return None

        # TODO: we can restrict to public or private here easily
        _, parts, offset = result

        # hostname = suffix
        if offset < 0:
            return ".".join(parts)

        return ".".join(parts[offset - 1 :])
