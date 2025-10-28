#!/usr/bin/env python3

from pathlib import Path

from ..startmeup import *

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

from .files import File
from .folders import Folder

class TempFile(File):
    def __enter__(self):
        self.path = Path(tempfile.mktemp())
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        try: self.path.unlink()
        except FileNotFoundError: pass

class TempFolder(Folder):
    def __enter__(self):
        self.path = Path(tempfile.mkdtemp())
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.path, ignore_errors=True)

