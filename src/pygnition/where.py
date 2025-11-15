#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

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


# ---------------------------
# System imports
# ---------------------------

from enum import auto, Enum
from functools import wraps
from inspect import getsourcefile
import os
from pathlib import Path
import sys

from ._imports import import_chain
from .interpreters import Interpreters, INTERPRETER
from .lists import first_after_last_digits

RUNNING_CLI = INTERPRETER in {Interpreters.CLI,
                              Interpreters.GATEWAY,
                              Interpreters.TKINTER,
                              Interpreters.UNKNOWN
                             }

RUNNING_JUPYTER = INTERPRETER == Interpreters.JUPYTER

RUNNING_CONSOLE = INTERPRETER in { Interpreters.CONSOLE,
                                   Interpreters.IPYTHON
                                 }

RUNNING_GATEWAY = INTERPRETER == Interpreters.GATEWAY


try:
    from pygnition.ignition import *
except (ImportError, ModuleNotFoundError) as e:
    try:
        sys.path.insert(0, PYGNITION_DIRECTORY)
        from pygnition.ignition import *
    except Exception:
        print(f'Pygnition import failed!')

PROJ_DATA = PACKAGE_PATH / 'data'
USER_DATA_DIR = Path.home() / f".{PACKAGE_NAME}"
USER_PREFS_DIR = USER_DATA_DIR / "etc"

# ---------------------------
# Runtime options
# ---------------------------
DEBUG = False
VERBOSE = False
WARNINGS = True
TESTING = False
# ---------------------------
# Command line flags
# ---------------------------
TESTING = bool({'-t', '--test'}.intersection(sys.argv))
# WARNINGS = bool({'-w', '--warnings'}.intersection(sys.argv)) or TESTING
DEBUG = bool({'-d', '--debug'}.intersection(sys.argv)) or TESTING
VERBOSE = bool({'-v', '--verbose'}.intersection(sys.argv)) or DEBUG

@auto_doc(AUTO_DOC_HEAD)
def display_where_info():
    """Test this module from any project directory that imports it."""
    print(f"Running: {PACKAGE_NAME}")
    print(f"Program path: {PACKAGE_PATH}")
    print(f"Ignition directory: {str(Path(__file__).parent.parent)}")
    print(f"Project directory: {str(PACKAGE_PATH.parent.parent.parent)}")
    print(f"Project data: {PROJECT_DATA_DIR}")
    print(f"User data directory: {USER_DATA_DIR}")
    print(f"Interpreter: {INTERPRETER.name}")
    print(f"RUNNING_CLI={RUNNING_CLI}, RUNNING_IN_JUPYTER={RUNNING_JUPYTER}, "
          f"RUNNING_CONSOLE={RUNNING_CONSOLE}, RUNNING_GATEWAY={RUNNING_GATEWAY}")

@auto_doc()
def cwd_mover(current_cwd=None):
    """
    Decorator that attaches the current working directory to the decorated
    function or method as the attribute `_CWD`.

    Works for standalone functions and class methods.
    """
    def decorator(func):
        _cwd = Path(current_cwd) if current_cwd else Path.cwd()

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # attach to both, so it can be accessed either way
        wrapper._CWD = _cwd
        try:
            func._CWD = _cwd
        except AttributeError:
            pass  # some built-in functions can't be assigned to

        return wrapper

    return decorator


if __name__ == "__main__":
    print('Running where')
    display_where_info()
