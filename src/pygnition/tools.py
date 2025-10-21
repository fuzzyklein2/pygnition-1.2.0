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


# from argparse import ArgumentParser as AP
from functools import partial, singledispatch, wraps
# from io import StringIO
import logging
import os
from pathlib import Path, PosixPath, WindowsPath
from subprocess import run

from rich import print as rp

from ._auto_doc import auto_doc
from .colors import DIR_BLUE, DIR_GREEN
from .picts import ASK_PICT, DEBUG_PICT, FOLDER_PICT, INFO_PICT, NEWLINE

@auto_doc("Return the current working directory.")
def cwd():
    return Path.cwd()

@auto_doc("Print `cwd()` and return it.")
def pwd():
    CWD = cwd()
    rp(f'{FOLDER_PICT}Current working directory: [{DIR_BLUE}]{CWD}[end]')
    return CWD

@auto_doc("Change the current working directory.")
def cd(p:str|Path)->Path|None:
    if not p.exists():
        warn(f'Directory [green]{str(p)}[end] does not exist!')
    os.chdir(p)
    return p

@auto_doc('Return the (supposedly) "public" members of the given object')
def public(obj)->list:
    return [s for s in dir(obj) if not s.startswith('_')]
    
def yes_or_no(question:str, message=None)->bool:
    if input(f'{(message + NEWLINE) if message else ''}'
             + f'{ASK_PICT + question} (y/n): ').lower() \
            in AFFIRMATIVES:
        return True
    return False

run_cmd = partial(run, encoding='utf-8', capture_output=True, check=True)

@singledispatch
def chk_cmd(arg):
    error(f"Bad `run` argument: {arg}")
    return None

@chk_cmd.register
def _(L:list):
    p = run_cmd(L)
    if p.stderr:
        print(p.stderr)
    if p.stdout:
        print(p.stdout)
    if p.returncode:
        print(f'{color_str('yellow', "WARNING")}! {L[1]} returned error code {p.returncode}')
    return p

@chk_cmd.register
def _(s:str) -> None:
    chk_cmd(s.split())

@singledispatch
def mkdir(arg):
    print(f'{STOP_PICT}{color_str('red', 'ERROR!')}: `mkdir` arg must be `str` or `Path`!')

@mkdir.register
def _(p:Path):
    p.mkdir(parents=True, exist_ok=True)

@mkdir.register
def _(s:str):
    mkdir(Path(s))

@singledispatch
def touch(arg):
    print(f'{STOP_PICT}{color_str('red', 'ERROR!')}: `touch` arg must be `str` or `Path`!')

@touch.register
def _(p:Path):
    p.touch(exist_ok=True)

@touch.register
def _(s:str):
    touch(Path(s))

@auto_doc()
def get_func_name(func):
    """Sets `name = ` the function's name."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.current_cmd = func.__name__.lstrip('do_')
        return func(self, *args, **kwargs)
    return wrapper

@auto_doc()
def get_func_name2(func):
    """Nearly identical to `get_func_name` but does not assume a Driver class
       called it."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return wrapper

@singledispatch
@auto_doc()
def subdirs(arg=None, all: bool = False) -> list[Path] | None:
    """
    Return a list of top-level subdirectories of `arg`
    (or the current directory if `arg` is None).

    Hidden directories are included only if `all=True`.
    """
    if arg is None:
        return subdirs(Path(os.curdir), all=all)

    error(f": subdirs : bad argument : {arg!r} : must be str or Path")


@auto_doc()
def _path_impl(p: Path, all: bool = False) -> list[Path] | None:
    """Return full Paths to top-level subdirectories within `p`."""
    if not p.exists() or not p.is_dir():
        error(f": subdirs : {p} : not a directory")

    dirs = [(p / name).resolve() for name in next(os.walk(p))[1]]
    if not all:
        dirs = [d for d in dirs if not d.name.startswith(".")]

    return dirs or None


# Register for concrete Path types
for cls in (Path, PosixPath, WindowsPath):
    try:
        subdirs.register(cls, _path_impl)
    except Exception:
        pass


@subdirs.register(str)
def _(s: str, all: bool = False) -> list[Path] | None:
    """Convert the str to a Path and call subdirs(p:Path)."""
    return subdirs(Path(s), all=all)
