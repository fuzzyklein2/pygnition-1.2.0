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

"""


from functools import singledispatch
import inspect

from IPython.display import display, Markdown

from .files import File
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

# Get the path of the currently running Jupyter notebook.

@auto_doc()
def find_proj_root():
    """ Move to the project root directory. """
    if cwd().stem == 'notebooks': cd('../')
    pwd()

@auto_doc()
def run_file(s: str # Name of the module to run. Should NOT include '.py' at the end.
            ):
    """ Run a python file. Should be expandable to include other script languages as well. """
    
    p = File(f'{cwd()}/src/{Path.cwd().name.split('-')[0]}/{s}.py').run()
    
    print(f"""{p.args} results:

Return code: {p.returncode}
""")
    if p.stderr:
        print(f"""Error output:

{p.stderr}
""")
    if p.stdout:
        print(f"""Standard output:

{p.stdout}
""")