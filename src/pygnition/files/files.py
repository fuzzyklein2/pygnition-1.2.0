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

# from functools import partial
import getpass
from io import StringIO
import mimetypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import magic
from rich import print as rp

# from ._metadata import PROJECT_NAME
# from .folders import Folder
from ..gui_tools import choose_file, zenity_available
from ..lumberjack import debug, error, info, stop, warn
from ..tools import cd, cwd, run_cmd
from ..where import cwd_mover

PROGRAM_NAME = PACKAGE_NAME

# --- Base File Factory ---
@auto_class_doc(AUTO_DOC_HEAD)
class File:
    _mime_registry: dict[str, type] = {}
    _ext_registry: dict[str, type] = {}
    _folder_registry: list[tuple[type, callable]] = []

    @auto_doc(AUTO_DOC_HEAD)
    def __new__(cls, p: str | Path | None = None):
        if cls is not File:
            return super().__new__(cls)
        if p is None:
            return super().__new__(cls)

        path = Path(p)

        # --- Folder detection ---
        if path.is_dir():
            from .folders import Folder  # delayed import to avoid circulars
            for subclass, predicate in cls._folder_registry:
                try:
                    if predicate(path):
                        return subclass(path)  # ✅ calls __init__
                except Exception:
                    continue
            return Folder(path)  # ✅ also calls __init__

        # --- Extension detection ---
        ext = path.suffix.lower()
        if ext in cls._ext_registry:
            return super().__new__(cls._ext_registry[ext])

        # --- MIME detection ---
        mime = cls._detect_mime(path)
        if mime:
            for pattern, subclass in cls._mime_registry.items():
                if mime.startswith(pattern):
                    return super().__new__(subclass)

        return super().__new__(cls)

    @auto_doc(AUTO_DOC_HEAD)
    def __init__(self, p: str | Path | None = None):
        self.path = Path(p) if p else None

    # --- MIME detection ---
    # @auto_doc(AUTO_DOC_HEAD)
    @staticmethod
    def _detect_mime(path: Path) -> str | None:
        try:
            import magic  # optional
            return magic.from_file(str(path), mime=True)
        except Exception:
            mime, _ = mimetypes.guess_type(path)
            return mime

    # --- Registration decorators ---
    # @auto_doc(AUTO_DOC_HEAD)
    @classmethod
    def register_mime(cls, pattern: str):
        def decorator(subclass):
            cls._mime_registry[pattern] = subclass
            return subclass
        return decorator

    # @auto_doc(AUTO_DOC_HEAD)
    @classmethod
    def register_ext(cls, *exts: str):
        def decorator(subclass):
            for e in exts:
                cls._ext_registry[e.lower()] = subclass
            return subclass
        return decorator

    # @auto_doc(AUTO_DOC_HEAD)
    @classmethod
    def register_folder(cls, predicate):
        def decorator(subclass):
            cls._folder_registry.append((subclass, predicate))
            return subclass
        return decorator

    # --- Delegation & Utilities ---
    @auto_doc(AUTO_DOC_HEAD)
    def __getattr__(self, name):
        if self.path and hasattr(self.path, name):
            return getattr(self.path, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    @auto_doc(AUTO_DOC_HEAD)
    def __truediv__(self, other):
        return File(self.path / other)

    @auto_doc(AUTO_DOC_HEAD)
    def __rtruediv__(self, other):
        return File(Path(other) / self.path)

    @auto_doc(AUTO_DOC_HEAD)
    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        return self.path == Path(other)

    @auto_doc(AUTO_DOC_HEAD)
    def __str__(self):
        return str(self.path) if self.path else "<no path>"

    @auto_doc(AUTO_DOC_HEAD)
    def __repr__(self):
        return f"{type(self).__name__}({self.path!r})"

    @auto_doc(AUTO_DOC_HEAD)
    def __fspath__(self):
        return str(self.path)

    @auto_doc(AUTO_DOC_HEAD)
    def output(self) -> str:
        if not self.path:
            return "[red]No path set[/red]"
        result = self.path.name
        if self.path.is_dir():
            result = f"[blue bold]{result}[/blue bold]"
        return result

    @auto_doc(AUTO_DOC_HEAD)
    def info(self, mime: bool = False, encoding: bool = False) -> str:
        """
        Return type information for a file, similar to the `file` command.
    
        :param path: Path to the file
        :param mime: If True, return MIME type (e.g., 'image/png')
        :param encoding: If True, return encoding info (e.g., 'utf-8')
        """
        if mime:
            ms = magic.Magic(mime=True)
        elif encoding:
            ms = magic.Magic(mime_encoding=True)
        else:
            ms = magic.Magic()
    
        return ms.from_file(str(Path(self.path)))
        
    @auto_doc(AUTO_DOC_HEAD)
    def is_hidden(self, p:str|Path) -> bool:
        return any(part.startswith('.') for part in Path(p).parts)
    
    @auto_doc(AUTO_DOC_HEAD)
    def is_visible(self, p:str|Path)->bool:
        return not is_hidden(p)
    
    # @auto_doc(AUTO_DOC_HEAD)
    # def info(self):
    #     if not self.path:
    #         return None
    #     return file_info(str(self.path.resolve()))

    @auto_doc(AUTO_DOC_HEAD)
    def mime(self):
        if not self.path:
            return None
        return self.info()

# Text / Source / Python / C Files

@File.register_folder(lambda p: not p.exists())
class MissingPath(File):
    def describe(self):
        return f"{self.path} (missing)"


if __name__ == '__main__':
    print(f"Running {Path(__file__).name}")
    from ..where import DEBUG, TESTING
    print(f'{TESTING=}')
    print(f'{DEBUG=}')
    print(f'{debug=}')
    if TESTING:
        debug('Running a PyFile...')
        p = PyFile().run()
        if not p:
            print("User cancelled.")
            # exit()
        else:
            code_color = 'red' if p.returncode else 'green'
            output = StringIO()
            rp(f"""
    [cyan]Called process results[/cyan]:
    Return code: [{code_color}]{p.returncode}[/{code_color}]""", file=output)
            if p.stderr:
                rp(f"""
    {('Error output: \n' + p.stderr + '\n') if p.stderr else ''}""", file=output)
            if p.stdout:
                rp(f"""
    {('Standard output: \n' + p.stdout + '\n') if p.stdout else ''}""", file=output)
            print(output.getvalue().strip())
            print()
        examples = [
    "/etc/hosts",
    "setup.py",
    "main.c",
    "/usr/share/pixmaps/debian-logo.png",
    "/usr/lib/python3.12",
    "/usr/src/linux",
]
        
        for e in examples:
            f = File(e)
            print(f"{f.path!s:40} -> {type(f).__name__}")

