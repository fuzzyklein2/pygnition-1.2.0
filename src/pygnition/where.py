#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# ---------------------------
# System imports
# ---------------------------

from enum import auto, Enum
from functools import wraps
from inspect import getsourcefile
import os
from pathlib import Path
import sys

from .imports import import_chain
from .interpreters import Interpreters
from .lists import first_after_last_digits

# ---------------------------
# Program environment
# ---------------------------
RUNNING_CLI = False
RUNNING_CONSOLE = False
RUNNING_IN_JUPYTER = False
RUNNING_GATEWAY = False

# ---------------------------
# Runtime options
# ---------------------------
DEBUG = False
VERBOSE = False
WARNINGS = False
TESTING = False

# ---------------------------
# Program variables
# ---------------------------
PROGRAM_NAME = "UNKNOWN"
PROGRAM_PATH = None
CALLING_MODULE = None

# ---------------------------
# Determine interpreter
# ---------------------------
CALLERS = import_chain()

if not sys.argv[0]: # Running console
    RUNNING_CONSOLE = True
    INTERPRETER = Interpreters.CONSOLE

    # for i, s in enumerate(CALLERS):
    #     if not s == 'code' and not s.startswith('_'):
    #         CALLING_MODULE = s
    #         break

    CALLING_MODULE = None

if "GATEWAY_INTERFACE" in os.environ: # Maybe, maybe not. CGI :/
    RUNNING_GATEWAY = True
    INTERPRETER = Interpreters.GATEWAY
    CALLING_MODULE = '__main__'

elif "ipykernel" in sys.modules: # Jupyter Lab
    RUNNING_IN_JUPYTER = True
    INTERPRETER = Interpreters.JUPYTER
    CALLING_MODULE = first_after_last_digits(CALLERS)

elif "IPython" in sys.modules: # ipython
    RUNNING_CONSOLE = True
    INTERPRETER = Interpreters.IPYTHON
    CALLING_MODULE = list(filter(lambda s: not (s.startswith('IPython') or s.startswith('traitlets') or s == 'ipython3')))[0]

elif sys.stdin.isatty(): # CLI
    if not RUNNING_CONSOLE:
        RUNNING_CLI = True
        # RUNNING_CONSOLE = True
        INTERPRETER = Interpreters.CLI
        CALLING_MODULE = '__main__'
        
else:
    # fallback
    RUNNING_CLI = True
    INTERPRETER = Interpreters.UNKNOWN

if CALLING_MODULE:
    try:
        PROGRAM_PATH = Path(sys.modules[CALLING_MODULE].__file__).resolve()
    except (KeyError, AttributeError):
        # Running in interactive console or notebook
        PROGRAM_PATH = None

if not PROGRAM_PATH:
    PROJECT_DIR = Path.cwd()
else:
    PROJECT_DIR = PROGRAM_PATH.parent.parent.parent

# if RUNNING_CLI or RUNNING_GATEWAY:
#     PROJECT_DIR = PROJECT_DIR.parent

PROGRAM_NAME = PROJECT_DIR.stem.split('-')[0]

# ---------------------------
# Project and user directories
# ---------------------------
PROJECT_NAME = PROGRAM_NAME

# ---------------------------
# Ensure that we have a PYGNITION_LOCATION environment variable for PyGTK
# and other scripts that require `python3` (3.12 at present), not >=3.13
# ---------------------------
PYGNITION_DIRECTORY = Path(getsourcefile(Interpreters)).parent.parent

try:
    from pygnition.ignition import *
except (ImportError, ModuleNotFoundError) as e:
    try:
        sys.path.insert(0, PYGNITION_DIRECTORY)
        from pygnition.ignition import *
    except Exception:
        print(f'Pygnition import failed!')

USER_DATA_DIR = Path.home() / f".{PROJECT_NAME}"
USER_PREFS_DIR = USER_DATA_DIR / "etc"

# ---------------------------
# Command line flags
# ---------------------------
DEBUG = bool({'-d', '--debug'}.intersection(sys.argv))
VERBOSE = bool({'-v', '--verbose'}.intersection(sys.argv))
WARNINGS = bool({'-w', '--warnings'}.intersection(sys.argv))
TESTING = bool({'-t', '--test'}.intersection(sys.argv))

@auto_doc()
def display_where_info():
    """Test this module from any project directory that imports it."""
    print(f"Running: {PROGRAM_NAME}")
    print(f"Program path: {PROGRAM_PATH}")
    print(f"Ignition directory: {PYGNITION_DIRECTORY}")
    print(f"Project directory: {PROJECT_DIR}")
    print(f"Project data: {PROJ_DATA}")
    print(f"User data directory: {USER_DATA_DIR}")
    print(f"Interpreter: {INTERPRETER.name}")
    print(f"RUNNING_CLI={RUNNING_CLI}, RUNNING_IN_JUPYTER={RUNNING_IN_JUPYTER}, "
          f"RUNNING_CONSOLE={RUNNING_CONSOLE}, RUNNING_GATEWAY={RUNNING_GATEWAY}")

# if not RUNNING_CLI and not RUNNING_GATEWAY:
#     display_where_info()

# ---------------------------
# Optional: display info if testing
# ---------------------------

# def cwd_mover(current_cwd=None):
#     """
#     Decorator that attaches the current working directory to the decorated function
#     as the attribute `_CWD`.

#     If no directory is provided, it captures the cwd at decoration time.
#     """
#     def decorator(func):
#         func._CWD = Path(current_cwd) if current_cwd else Path.cwd()
#         return func
#     return decorator

def cwd_mover(current_cwd=None):
    """
    Decorator that attaches the current working directory to the decorated
    function or method as the attribute `_CWD`.

    Works for standalone functions and class methods.
    """
    def decorator(func):
        cwd = Path(current_cwd) if current_cwd else Path.cwd()

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # attach to both, so it can be accessed either way
        wrapper._CWD = cwd
        try:
            func._CWD = cwd
        except AttributeError:
            pass  # some built-in functions can't be assigned to

        return wrapper

    return decorator


if __name__ == "__main__":
    print('Running where')
    display_where_info()
