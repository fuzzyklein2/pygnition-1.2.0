#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PROJECT_NAME}.{MODULE_NAME}
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


import sys
# from rich import print as rp

@auto_doc("Return any piped input.")
def get_piped_input() -> str|None:
    if not sys.stdin.isatty():
        INPUT = sys.stdin.read()
        return INPUT
    return None

if __name__ == '__main__':
    from rich import print as rp
    
    from .picts import DEBUG_PICT, INFO_PICT

    PROGRAM_PATH = Path(__file__)
    
    print(f"{INFO_PICT}Testing {PROGRAM_PATH.name if PROGRAM_PATH else Path(__file__).name}\n")
    rp(f"{DEBUG_PICT}[bold][cyan]Input[/cyan][/bold]:\n")

    # rp(f"[bold]{DEBUG_PICT}{color_str('cyan', 'Input')}[/bold]:\n")
    print(get_piped_input())
