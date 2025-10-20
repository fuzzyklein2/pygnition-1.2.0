#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️ WARNING! ⚠️ ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PKG_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {str(last_saved_datetime(__file__).date()).split('.')[0]}

## Description

This module defines the Workshop class.

## Typical Use
```python
app = Workshop()
app.run()

Notes
-----
You can include implementation notes, dependencies, or version-specific
details here.

"""

import atexit

from rich import print as rp

from .lumberjack import debug, error, info, warn, stop
from .picts import CHECK_PICT, CONSTRUCTION_PICT, WARNING_PICT, WAVE_PICT
from .settings import Settings
from .where import PROGRAM_NAME

class Program(Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        debug(f'Running {self.program_name}')
        self.dump()

    def under_construction(self):
        rp(f"{WARNING_PICT}[yellow bold]WARNING[/yellow bold]: {PROGRAM_NAME} is under construction! {CONSTRUCTION_PICT}")


if __name__ == '__main__':
    Program().run()
