# static-sitegen main

import os
import sys
import logging
import argparse

import common
from file_operations import create_site

parser = argparse.ArgumentParser(description="Static Site Generator", prog="static-sitegen", add_help=False)
parser.add_argument('--build', nargs="?", const="/", help='Generate the site in "docs", add optional argument string to specify basepath')
parser.add_argument('--console', action='store_true', help='Enable verbose output, does not affect logging')
args, remaining = parser.parse_known_args()

logging.basicConfig(
    filename=os.path.join(common.ABSPATH, "logs", "static_sitegen.log"),      # Name of the log file
    filemode='a',                # 'a' to append, 'w' to overwrite
    format='%(asctime)s %(levelname)s: %(funcName)s: %(message)s',  # Log message format
    level=logging.INFO          # Minimum log level to capture
)

def main():
    if args.console:
        common.set_console_mode(True)

    if args.build:
        common.set_build_mode(True)
        common.set_build_basepath(args.build)

    header = '-----------------------------\n--- Static Site Generator ---\n-----------------------------'

    common.console_print(header, True)

    create_site()

if __name__ == "__main__":
    main()
