#!/usr/bin/env python3

from importlib import import_module
from pathlib import Path

from ._auto_doc import auto_class_doc, auto_doc, AUTO_DOC_HEAD
from ._imports import import_chain

def get_project_nv(s: str | Path) -> (str, str):
    # debug(f'{type(s)=}')
    COMPONENTS = Path(s).resolve().name.split('-')
    return ('-'.join(COMPONENTS[:-1]), COMPONENTS[-1])

PACKAGE_NAME = import_chain()[0]
if PACKAGE_NAME.startswith('_pyrepl'):
    PACKAGE_NAME, VERSION = get_project_nv('.')
    print(PACKAGE_NAME)
    
try:
    _metadata = import_module(f'{PACKAGE_NAME}._metadata')
    globals().update(vars(_metadata))
except ModuleNotFoundError: # Most likely happens in a Jupyter notebook or a console
                            # Appears to happen in pydoc as well.
    from ._metadata import *

__doc__ = f"""The 🔥  pygnition 🔥  package sets up an environment for any script that imports it.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

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

## [GitHub]({get_upstream_url()})

"""

CWD = Path.cwd()

