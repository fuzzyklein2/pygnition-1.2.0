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

from abc import ABC, abstractmethod
import tkinter as tk

from . import get_root
from .constants import *

class Dialog(ABC):
    def __init__(self, title: str = EMPTY_STR, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT):
        self.title = title
        self.width = width
        self.height = height
        self.parent = get_root()
        self.window = None

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError

    def _center_window(self):
        self.window.update_idletasks()
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - self.width) // 2
        y = (screen_h - self.height) // 2
        self.window.geometry(f"{self.width}x{self.height}+{x}+{y}")
