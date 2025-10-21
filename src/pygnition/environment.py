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


import os
from pprint import pformat

from ._metadata import PROJECT_NAME
from .utils import *

class Environment(dict):
    def __init__(self, prefix=PROJECT_NAME.upper()+'_', *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        KEYS = grep(prefix, os.environ.keys())

        # ENV = dict()

        for k in KEYS:
            # print(f'$ENVIRONMENT_LOGFILE: {os.environ["ENVIRONMENT_LOGFILE"]}')
            self[k.lstrip(prefix).lower()] = os.environ[k]

    def dumps(self):
        return pformat(self)

if __name__ == '__main__':
    print(f'{PROGRAM_NAME=}')
    print(f"""Environtment variables:

{pformat(Environment())}
""")
    # print(f'{type(os.environ)=}')
