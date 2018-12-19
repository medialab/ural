# =============================================================================
# Ural Normalize CLI Action
# =============================================================================
#
# Logic of the normalize CLI action enabling the user to normalize the urls of
# a CSV file column.
#
import csv

from ural.cli.utils import custom_reader
from ural import normalize_url


def normalize_action(namespace):
    sort_query = not namespace.no_query_sort
    strip_authentication = not namespace.keep_authentication
    strip_trailing_slash = namespace.strip_trailing_slash
    strip_index = not namespace.keep_index

    headers, position, reader = custom_reader(namespace.file, namespace.column)

    headers.append(namespace.column + "_normalized")
    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    for line in reader:
        url = line[position]
        line.append(normalize_url(url, sort_query=sort_query, strip_authentication=strip_authentication,
                                  strip_trailing_slash=strip_trailing_slash, strip_index=strip_index))
        writer.writerow(line)
