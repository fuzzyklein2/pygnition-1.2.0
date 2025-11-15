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


# from argparse import ArgumentParser as AP
from functools import partial, singledispatch, wraps
from glob import glob
# from io import StringIO
import logging
import os
from pathlib import Path, PosixPath, WindowsPath
import shlex
from subprocess import run

from rich import print as rp
from rich.columns import Columns
from rich.console import Console

from ._auto_doc import auto_doc
from .colors import DIR_BLUE, DIR_GREEN
from .picts import ASK_PICT, DEBUG_PICT, ERROR_PICT, FOLDER_PICT, INFO_PICT, NEWLINE, WARNING_PICT

@auto_doc(AUTO_DOC_HEAD)
def cwd():
    """Return the current working directory."""
    return Path.cwd()

@auto_doc(AUTO_DOC_HEAD)
def pwd():
    """Print `cwd()` and return it."""
    CWD = cwd()
    rp(f'{FOLDER_PICT}Current working directory: [{DIR_BLUE}]{CWD}[end]')
    # return CWD

@auto_doc(AUTO_DOC_HEAD)
def cd(p:str|Path)->Path|None:
    """Change the current working directory."""
    p = Path(p)
    if not p.exists():
        rp(f'{WARNING_PICT}[yellow]WARNING[/yellow]: Directory [green]{str(p)}[end] does not exist!')
    os.chdir(p)
    return p

@auto_doc(AUTO_DOC_HEAD)
def columnize(L:list[str]):
    """ Arrange the list of strings into columns. `rich` handles spacing of its color strings. """
    Console().print(Columns(sorted(L), expand=True, equal=True))

@auto_doc(AUTO_DOC_HEAD)
def public(obj)->list:
    """Return the (supposedly) "public" members of the given object."""
    return sorted([s for s in dir(obj) if not s.startswith('_')])
    
def yes_or_no(question:str, message=None)->bool:
    if input(f'{(message + NEWLINE) if message else ''}'
             + f'{ASK_PICT + question} (y/n): ').lower() \
            in AFFIRMATIVES:
        return True
    return False

run_cmd = partial(run, encoding='utf-8', capture_output=True, check=False, shell=True)

@singledispatch
def chk_cmd(arg):
    error(f"Bad `run` argument: {arg}")
    return None

@chk_cmd.register
def _(L:list):
    # print('Running `chk_cmd(list)`')
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
    # print('Running `chk_cmd(str)`')
    # Expand environment vars
    s = os.path.expandvars(s)

    # Split into args
    parts = shlex.split(s)

    # Expand wildcards manually (glob)
    expanded = []
    for part in parts:
        if any(ch in part for ch in "*?[]"):
            expanded.extend(glob(part))
        else:
            expanded.append(part)

    # 🔴 Call run_cmd directly — NOT chk_cmd again
    return run_cmd(expanded)

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

    rp(f"{ERROR_PICT}[red]ERROR[/red]: subdirs : bad argument : {arg!r} : must be str or Path")


@auto_doc()
def _path_impl(p: Path, all: bool = False) -> list[Path] | None:
    """Return full Paths to top-level subdirectories within `p`."""
    if not p.exists() or not p.is_dir():
        rp(f"{ERROR_PICT}[red]ERROR[/red]: subdirs : {p} : not a directory")

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

@auto_doc(AUTO_DOC_HEAD)
def run_python(src):
    try:
        code = compile(src, "<input>", "eval")
        return eval(code)
    except SyntaxError:
        exec(src)

def grep(s: str, f: str) -> str | None:
    """ Search for `s` in the given `f`iles. """
    
    # Expand env vars and globs manually
    f = os.path.expandvars(f)
    files = glob(f)
    if not files:
        print(f"(no files match {f})")
        return None

    # Build grep argument list directly
    cmd = ["grep", "-E", "-n", s, *files]
#    print("Running:", " ".join(cmd))

    p = run(cmd, encoding="utf-8", capture_output=True)
    if p.returncode == 0:
        print(p.stdout, end="")
    elif p.returncode == 1:
        print(f"(no matches found for '{s}')")
    elif p.returncode == 2:
        print(f"❌ grep error:\n{p.stderr}")
    return p.stdout or None

def find_def(s: str|obj, f: str) -> str | None:
    """Search for variable, def, or class definitions matching `s` in file(s) `f`."""
    if type(s) is not str:
        s = s.__name__
    # Build grep argument list directly
    pattern = f"{s} = |def {s}|class {s}"
    grep(pattern, f)