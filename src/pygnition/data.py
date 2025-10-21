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

from pathlib import Path

class PackageData:
    """
    Simple data manager for package files.

    Attributes
    ----------
    base_dir : Path
        Base directory for data files.
    """

    def __init__(self, base_dir: str | Path = None):
        # Default to ./data relative to this file
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent / "data"

    def get(self, filename: str, mode: str = "text", default=None):
        """
        Read a file from the package data directory.

        Parameters
        ----------
        filename : str
            Name of the file relative to base_dir.
        mode : str
            "text" (default) or "bytes".
        default : any
            Value to return if file does not exist. Raises FileNotFoundError if None.

        Returns
        -------
        str or bytes
            Contents of the file.
        """
        path = self.base_dir / filename

        if not path.exists():
            if default is not None:
                return default
            raise FileNotFoundError(f"{filename} not found in {self.base_dir}")

        if mode == "text":
            return path.read_text()
        elif mode == "bytes":
            return path.read_bytes()
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def list(self, pattern="*"):
        """
        List files in the base directory matching the glob pattern.

        Parameters
        ----------
        pattern : str
            Glob pattern, supports recursive **/*.

        Returns
        -------
        List[Path]
            List of Path objects.
        """
        return list(self.base_dir.glob(pattern))
