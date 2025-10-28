#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PACKAGE_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {LAST_SAVED_DATE}

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

"""


import ast
from functools import singledispatch

from .picts import *

def parse_file_for_docstr(s:str) -> str | None:
    return ast.get_docstring(ast.parse(s))

@singledispatch
def get_docstring_from_file(arg) -> str | None:
    raise TypeError(f"Unsupported type: {type(arg)}")

@get_docstring_from_file.register
def _(p: Path) -> str | None:
    source = p.read_text(encoding='utf-8')
    return parse_file_for_docstr(source)

@get_docstring_from_file.register
def _(s: str) -> str | None:
    source = Path('__init__.py').read_text(encoding='utf-8')
    return parse_file_for_docstr(source)

def remove_tag(s:str) -> str:
    return ' '.join(s.strip().split()[1:])

def grep(pattern, s):
    if isinstance(s, str):
        lines = s.splitlines()
    else:
        lines = s
    return [line for line in lines if line.startswith(pattern)]

def is_rich_color(name: str) -> bool:
    try:
        Color.parse(name)
        return True
    except Exception:
        return False
        
def color_str(color, s:str) -> str:
    if is_rich_color(color):
        buffer = StringIO()
        console = Console(file=buffer, color_system='truecolor', force_terminal=True)
        console.print(f"[{color}]{s}")
        return buffer.getvalue().strip()
    else:
        return f'[red]ERROR![end] Invalid color!'

@auto_doc()
def get_full_name() -> str:
    """Return the current user's full name, falling back to username if not set."""
    try:
        pw = pwd.getpwuid(os.getuid())
        full_name = pw.pw_gecos.split(',')[0].strip()
        if full_name:
            return full_name
    except Exception:
        pass
    # Fallbacks
    return os.getenv("USER") or os.getenv("LOGNAME") or "Unknown User"
