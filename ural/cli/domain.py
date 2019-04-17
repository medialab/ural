# =============================================================================
# Ural Domain CLI Action
# =============================================================================
#
# Logic of the domain CLI action enabling the user to extract the domain name
# of urls contained in a CSV column.
#
import csv

from ural.cli.utils import custom_reader
from ural import get_domain_name


def domain_action(namespace):
    headers, position, reader = custom_reader(namespace.file, namespace.column)

    headers.append(namespace.column + "_domain")
    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    for line in reader:
        url = line[position]
        line.append(get_domain_name(url))
        writer.writerow(line)
