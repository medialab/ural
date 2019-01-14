# =============================================================================
# Ural Join CLI Action
# =============================================================================
#
# Logic of the join CLI action enabling the user to join 2 csv files according
# to the urls each of them contains.
#
import csv

from ural.cli.utils import custom_reader
from ural.lru_trie import LRUTrie


def join_action(namespace):
    col1 = namespace.col1
    file1 = namespace.file1
    col2 = namespace.col2
    file2 = namespace.file2

    file1_headers, file1_position, file1_reader = custom_reader(
        namespace.file1, namespace.col1)
    file2_headers, file2_position, file2_reader = custom_reader(
        namespace.file2, namespace.col2)
    headers = file1_headers + file2_headers
    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    trie = LRUTrie()

    for line in file1_reader:
        url = line[file1_position]
        print(url)
        # metadata = {i: line[i] for i in line if i != col1}
        metadata = line
        trie.set(url, metadata)

    for line in file2_reader:
        metadata = line
        trie_metadata = trie.match(line[file2_position])
        if trie_metadata:
            row = trie_metadata + metadata
        else:
            row = ['' for i in range(len(file1_headers))] + metadata
        writer.writerow(row)
