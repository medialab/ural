# =============================================================================
# TrieDict
# =============================================================================
#
# A simple Python implementation of a (prefix, value) Trie.
#
NULL = object()


class TrieDictNode(object):
    __slots__ = ('children', 'value')

    def __init__(self):
        self.children = None
        self.value = NULL


class TrieDict(object):
    __slots__ = ('__root', '__size')

    def __init__(self):
        self.__root = TrieDictNode()
        self.__size = 0

    def __len__(self):
        return self.__size

    def __setitem__(self, prefix, value):
        node = self.__root

        for token in prefix:

            if node.children is None:
                child = TrieDictNode()

                node.children = {
                    token: child
                }

                node = child
                continue

            child = node.children.get(token)

            if child is not None:
                node = child
            else:
                child = TrieDictNode()

                node.children[token] = child
                node = child

        if node.value is NULL:
            self.__size += 1

        node.value = value

    def get(self, prefix, default=None):
        node = self.__root

        for token in prefix:
            if node.children is None:
                return default

            child = node.children.get(token)

            if child is None:
                return default

            node = child

        if node.value is not NULL:
            return node.value

        return default

    def __getitem__(self, prefix):
        node = self.__root

        for token in prefix:
            if node.children is None:
                raise KeyError(prefix)

            child = node.children.get(token)

            if child is None:
                raise KeyError(prefix)

            node = child

        if node.value is not NULL:
            return node.value

        raise KeyError(prefix)

    def longest_matching_prefix_value(self, prefix):
        node = self.__root

        last_value = NULL

        for token in prefix:

            if node.value is not NULL:
                last_value = node.value

            if node.children is None:
                break

            child = node.children.get(token)

            if child is None:
                break

            node = child

        if node.value is not NULL:
            return node.value

        return last_value if last_value is not NULL else None

    def items(self):
        stack = [(self.__root, [])]

        while len(stack) > 0:
            node, prefix = stack.pop()

            if node.value is not NULL:
                yield (prefix, node.value)

            if node.children is None:
                continue

            for token, child in node.children.items():
                stack.append((child, prefix + [token]))

    def prefixes(self):
        stack = [(self.__root, [])]

        while len(stack) > 0:
            node, prefix = stack.pop()

            if node.value is not NULL:
                yield prefix

            if node.children is None:
                continue

            for token, child in node.children.items():
                stack.append((child, prefix + [token]))

    def values(self):
        stack = [self.__root]

        while len(stack) > 0:
            node = stack.pop()

            if node.value is not NULL:
                yield node.value

            if node.children is None:
                continue

            stack.extend(node.children.values())

    def __iter__(self):
        return self.items()
