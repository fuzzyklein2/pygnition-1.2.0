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

## [GitHub]({get_upstream_url()})

"""

import pwd

@auto_doc(AUTO_DOC_HEAD)
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
    return os.getenv("USER") or os.getenv("LOGNAME") or "Unknown User" # The full name of the user if it's registered with the system; otherwise, just the username.

# import sys
# from rich import print as rp

if __name__ == '__main__':
    print(f"Hello, {get_full_name}!")