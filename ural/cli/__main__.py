#!/usr/bin/env python
# =============================================================================
# Ural CLI Endpoint
# =============================================================================
#
# CLI Interface of the Ural library.
#
import sys
from argparse import ArgumentParser, FileType

from ural.cli.normalize import normalize_action
from ural.cli.join import join_action


SUBPARSERS = {}


def main():
    parser = ArgumentParser(prog='ural')
    subparsers = parser.add_subparsers(
        help='action to execute', title='actions', dest='action')

    normalize_subparser = subparsers.add_parser(
        'normalize', description='Normalize the urls of a given CSV column.')
    normalize_subparser.add_argument('column', help='column')
    normalize_subparser.add_argument(
        'file', help='csv file containing the urls to normalize', type=FileType('r'), default=sys.stdin, nargs='?')
    normalize_subparser.add_argument(
        '-o', '--output', help='output file', type=FileType('w'), default=sys.stdout)
    normalize_subparser.add_argument(
        '--no-query-sort', action='store_true', help='do not sort query items', default=False)
    normalize_subparser.add_argument(
        '--keep-authentication', action='store_true', help='do not drop authentication', default=False)
    normalize_subparser.add_argument(
        '--strip-trailing-slash', action='store_true', help='drop trailing slash', default=False)
    normalize_subparser.add_argument(
        '--keep-index', action='store_true', help='do not drop trailing index at the end of the url', default=False)
    SUBPARSERS['normalize'] = normalize_subparser

    join_subparser = subparsers.add_parser(
        'join', description='Join 2 csv files according to their urls columns.')
    join_subparser.add_argument(
        'column1', help='name of the url column of the first file')
    join_subparser.add_argument(
        'file1', help='first csv file', type=FileType('r'), default=sys.stdin, nargs='?')
    join_subparser.add_argument(
        'column2', help='name of the url column of the second file')
    join_subparser.add_argument(
        'file2', help='second csv file', type=FileType('r'), default=sys.stdin, nargs='?')
    join_subparser.add_argument(
        '-o', '--output', help='output file', type=FileType('w'), default=sys.stdout)
    join_subparser.add_argument(
        '-s', '--select', nargs='+', help='columns of the first file wanted in the output')
    join_subparser.add_argument(
        '--large-cells', action='store_true', help='activate if the csv contains huge cells (>131072)', default=False)
    SUBPARSERS['join'] = join_subparser

    help_suparser = subparsers.add_parser('help')
    help_suparser.add_argument('subcommand', help='name of the subcommand')
    SUBPARSERS['help'] = help_suparser

    args = parser.parse_args()

    if args.action == 'help':
        target_subparser = SUBPARSERS.get(args.subcommand)

        if target_subparser is None:
            parser.print_help()
        else:
            target_subparser.print_help()

    if args.action == 'normalize':
        normalize_action(args)

    if args.action == 'join':
        join_action(args)

    if args.action is None:
        parser.print_help()


if __name__ == '__main__':
    main()
