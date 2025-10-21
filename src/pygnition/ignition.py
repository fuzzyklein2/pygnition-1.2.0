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



# from enum import auto, Enum
# from glob import glob
# import logging
# import os
# from pathlib import Path
# from pprint import pformat
# from subprocess import run
# import sys


# ap = AP(prog=PROGRAM, description=DESCRIPTION, epilog=EPILOG)
# for option in STD_OPTS:
#     ap.add_argument(*option[0], **option[1])

# ARGS = ap.parse_args(sys.argv[1:])

# if __debug__:
#     print(f'{ARGS.debug=}')
#     print(f'{ARGS.verbose=}')

# DEBUG = bool({'-d', '--debug'}.intersection(sys.argv))
# VERBOSE = bool({'-v', '--verbose'}.intersection(sys.argv))
# WARNINGS = bool({'-w', '--warnings'}.intersection(sys.argv))
# TESTING = bool({'-t', '--test'}.intersection(sys.argv))

if __name__ == '__main__':
    if VERBOSE:
        print(f"{WARNING_PICT}{color_str('yellow', "WARNING!")} {color_str('green', PROGRAM)} is under construction!{CONSTRUCTION_PICT}")

