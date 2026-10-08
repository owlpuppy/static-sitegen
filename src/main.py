# static-sitegen main

import os
import sys
import logging

import common

logging.basicConfig(
    filename=os.path.join(common.ABSPATH, "logs", "static_sitegen.log"),      # Name of the log file
    filemode='a',                # 'a' to append, 'w' to overwrite
    format='%(asctime)s %(levelname)s: %(funcName)s: %(message)s',  # Log message format
    level=logging.INFO          # Minimum log level to capture
)

from file_operations import duplicate_files, generate_pages

def main():
    duplicate_files()
    generate_pages("template.html")

if __name__ == "__main__":
    main()
