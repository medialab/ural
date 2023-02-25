class TLDTrieNode(object):
    __slots__ = ("children", "exception", "leaf", "private")

    def __init__(self):
        self.children = None
        self.exception = None
        self.leaf = False
        self.private = False


class TLDTrie(object):
    def __init__(self):
        self.root = TLDTrieNode()

    def add(self, tld, private=False):
        node = self.root

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
