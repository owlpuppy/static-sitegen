# static_sitegen src/common

import sys
import os
import argparse
import logging

ABSPATH = os.path.abspath("./")

logger = logging.getLogger("static-sitegen")

parser = argparse.ArgumentParser(description="Static Site Generator", prog="static-sitegen", add_help=False)
parser.add_argument('--build', nargs="?", const="/", help='Generate the site in "docs", add optional argument string to specify basepath')
parser.add_argument('--console', action='store_true', help='Enable verbose output, does not affect logging')
args, remaining = parser.parse_known_args()

# multiuse functions

def html_specialchars_encode(text: str) -> str:
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;").replace("<", "&lt;").replace(">", "&gt;")

def console_print(message: str, override: bool = False) -> None:
    if override:
        message = f'\n{message}'
    if args.console or override:
        print(message)
