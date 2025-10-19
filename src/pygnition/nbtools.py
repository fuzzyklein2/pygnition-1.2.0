#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
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
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

"""

from functools import singledispatch

from IPython.display import display, Markdown

from .lumberjack import *

@get_func_name2
@auto_doc()
@singledispatch
def display_source(arg)->None:
    """Print an error message and depart."""
    error(f': {name} : bad argument : {arg} : Argument must be str or Path')

@get_func_name2
@auto_doc()
@display_source.register
def _(s:str, lang:str='python')->None:
    display(Markdown(f'```{lang}\n{s}'))

@get_func_name2
@auto_doc()
@display_source.register
def _(p:Path, lang:str='python')->None:
    display_source(p.read_text(), lang=lang)

@get_func_name2
@auto_doc()
@display_source.register
def _(obj:object, lang:str='python')->None:
    display_source(inspect.getsource(obj))