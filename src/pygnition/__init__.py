#!/usr/bin/env python3

from importlib import import_module

from ._auto_doc import auto_doc
from ._imports import import_chain

PACKAGE_NAME = import_chain()[0]

_metadata = import_module(f'{PACKAGE_NAME}._metadata')
globals().update(vars(_metadata))

__doc__ = f"""The 🔥  pygnition 🔥  package sets up an environment for any script that imports it.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{_metadata.VERSION}

## Author

{AUTHOR}

## Date

{LAST_SAVED_DATE}

## Usage

```python
from pygnition.program import Program
Program().run()

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.
"""

CWD = Path.cwd()