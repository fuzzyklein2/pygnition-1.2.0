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
from ..where import cwd_mover

@File.register_mime("text/")
class TextFile(File):
    def read_lines(self) -> list[str]:
        return self.path.read_text(errors='ignore').splitlines() if self.path else []

    def write_lines(self, lines: list[str]):
        self.path.write_text('\n'.join(lines))

    def sed(self, inplace=False)-> bool:
        pass

@File.register_ext(".cfg")
class ConfigFile(TextFile):
    """Simple key=value config file handler."""
    
    def read(self) -> dict[str, str]:
        data = {}
        if not self.path or not self.path.exists(): 
            return data
        for line in self.path.read_text().splitlines():
            line = line.split('#', 1)[0].strip()  # strip comments
            if not line: 
                continue
            key, sep, value = line.partition('=')
            if sep:
                data[key.strip()] = value.strip()
        return data

    def write(self, data: dict[str, str]):
        lines = [f"{k} = {v}" for k, v in data.items()]
        self.path.write_text('\n'.join(lines))

class SrcFile(TextFile):
    """Generic source file."""
    pass

# C source files
@File.register_ext(".c", ".h")
class CFile(SrcFile):
    """Represents a C source or header file."""
    def compile(self, output: str | None = None) -> subprocess.CompletedProcess:
        """Compile the C file with gcc."""
        if output is None:
            output = self.path.stem
        return run_cmd(["gcc", str(self.path), "-o", str(output)])

