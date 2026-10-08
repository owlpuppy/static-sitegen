# static_sitegen src/common

import os
import logging

ABSPATH = os.path.abspath("./")
BUILD_DEST = 'docs'

logger = logging.getLogger("static-sitegen")

# multiuse functions

def html_specialchars_encode(text: str) -> str:
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;").replace("<", "&lt;").replace(">", "&gt;")
