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
    headers, position, reader = custom_reader(namespace.file, namespace.column)

    headers.append(namespace.column + "_normalized")
    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    for line in reader:
        url = line[position]
        line.append(normalize_url(url))
        writer.writerow(line)
