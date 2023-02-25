from __future__ import print_function

from argparse import ArgumentParser

parser = ArgumentParser(prog="ural")
subparsers = parser.add_subparsers(dest="action")
_ = subparsers.add_parser(
    "upgrade",
    help="Run this command to upgrade ural's TLD utilities wrt latest Mozilla data.",
)

cli_args = parser.parse_args()

if cli_args.action == "upgrade":
    from ural.tld import upgrade

    upgrade()
