# static_sitegen src/common

import sys
import os
import logging

# global statics

ABSPATH = os.path.abspath("./")

# global internals

_console_mode = False
_build_mode = False
_build_basepath = '/'

# loggers

logger = logging.getLogger("static-sitegen")

# global internal setters

def set_console_mode(flag: bool = False) -> None:
    if not isinstance(flag, bool):
        raise ValueError("flag must be type: bool")
    global _console_mode
    _console_mode = flag

def set_build_mode(flag: bool = False) -> None:
    if not isinstance(flag, bool):
        raise ValueError("flag must be type: bool")
    global _build_mode
    _build_mode = flag

def set_build_basepath(text: str = '/') -> None:
    if not isinstance(text, str):
        raise ValueError("text must be type: str")
    global _build_basepath
    _build_basepath = text

# multiuse functions

def html_specialchars_encode(text: str) -> str:
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;").replace("<", "&lt;").replace(">", "&gt;")

def console_print(message: str, override: bool = False) -> None:
    if override:
        message = f'\n{message}'
    if _console_mode or override:
        print(message)
