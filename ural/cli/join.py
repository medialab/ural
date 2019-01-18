# =============================================================================
# Ural Join CLI Action
# =============================================================================
#
# Logic of the join CLI action enabling the user to join 2 csv files according
# to the urls each of them contains.
#
import csv
import sys

from ural.cli.utils import custom_reader
from ural.lru_trie import LRUTrie


def join_action(namespace):

    if namespace.large_cells:
        csv.field_size_limit(sys.maxsize)
    file1_headers, file1_position, file1_reader = custom_reader(
        namespace.file1, namespace.column1)
    file2_headers, file2_position, file2_reader = custom_reader(
        namespace.file2, namespace.column2)
    if namespace.select:
        headers = namespace.select + file2_headers
    else:
        headers = file1_headers + file2_headers
    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    trie = LRUTrie()

    for line in file1_reader:
        url = line[file1_position]
        if namespace.select:
            try:
                metadata = [line[file1_headers.index(
                    x)] for x in namespace.select]
            except ValueError as e:
                print("Woops, the header '" + str(e)
                      [1:-16] + "' doesn't exist !")
                sys.exit(1)
        else:
            metadata = line
        trie.set(url, metadata)

    for line in file2_reader:
        metadata = line
        trie_metadata = trie.match(line[file2_position])
        if trie_metadata:
            row = trie_metadata + metadata
        elif namespace.select:
            row = ['' for i in range(len(namespace.select))] + metadata
        else:
            row = ['' for i in range(len(file1_headers))] + metadata
        writer.writerow(row)
