#!/usr/bin/env python3

from ._initools import *

__doc__ = f"""The 🔥  pygnition 🔥  package sets up an environment for any script that imports it.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

## Author

{AUTHOR}

## Date

{last_saved_datetime(__file__).date()}

## Usage

```python
from {PKG_NAME}.program import Program
Program().run()

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.
"""
