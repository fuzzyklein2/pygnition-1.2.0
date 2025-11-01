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

@auto_class_doc(AUTO_DOC_HEAD)
class Folder(File):
    def list(self):
        return [File(p) for p in self.path.iterdir()]

    def tree(self, depth: int = 2):
        def _walk(p, d):
            if d < 0: return
            for f in p.iterdir():
                print('  ' * (depth-d) + f.name)
                if f.is_dir():
                    _walk(f, d-1)
        _walk(self.path, depth)

@File.register_folder(lambda p: (p / "__init__.py").exists())
class PyPackage(Folder):
    def info(self):
        return f"{self.path} (Python package)"

@File.register_folder(lambda p: any(p.glob("*.c")))
class CProjectDir(Folder):
    def info(self):
        return f"{self.path} (C project directory)"

@File.register_folder(lambda p: (p / 'index.html').exists())
class WebSiteFolder(Folder):
    def info(self):
        return f"{self.path} (C project directory)"
