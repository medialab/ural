# =============================================================================
# TrieDict
# =============================================================================
#
# A simple Python implementation of a (prefix, value) Trie.
#
NULL = object()


class TrieDictNode(object):
    __slots__ = ("children", "value", "counter")

    def __init__(self):
        self.children = None
        self.value = NULL
        # Counts the number of items in the node's children
        self.counter = 0


class TrieDict(object):
    __slots__ = "__root"

    def __init__(self):
        self.__root = TrieDictNode()

    def __len__(self):
        return self.__root.counter

    def __setitem__(self, prefix, value):
        node = self.__root

        visited_nodes = []

        for token in prefix:

            if node.children is None:
                child = TrieDictNode()

                node.children = {token: child}

                visited_nodes.append(node)
                node = child
                continue

            child = node.children.get(token)

            if child is not None:
                visited_nodes.append(node)
                node = child
            else:
                child = TrieDictNode()

                node.children[token] = child
                visited_nodes.append(node)
                node = child

        if node.value is NULL:
            for n in visited_nodes:
                n.counter += 1

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

    def set_and_prune_if_shorter(self, prefix, value):

        node = self.__root

        visited_nodes = []

        for token in prefix:

            # Check if we try to add a longer prefix
            if node.value is not NULL:
                return

            if node.children is None:
                child = TrieDictNode()

                node.children = {token: child}
                visited_nodes.append(node)
                node = child
                continue

            child = node.children.get(token)

            if child is not None:
                visited_nodes.append(node)
                node = child
            else:
                child = TrieDictNode()

                node.children[token] = child
                visited_nodes.append(node)
                node = child

        # Trie already has longer prefixes of the prefix we are trying to add : we delete those prefixes and new (shortest) one
        if node.children is not None:
            node.children = None
            for n in visited_nodes:
                n.counter -= node.counter - 1
            node.counter = 0

        # We add a prefix with no longer prefixes in the Trie
        elif node.value is NULL:
            for n in visited_nodes:
                n.counter += 1

        node.value = value
