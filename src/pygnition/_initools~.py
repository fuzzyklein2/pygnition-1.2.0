import ast
from datetime import date
from datetime import datetime as dt
from functools import singledispatch, wraps
import inspect
from pathlib import Path
import subprocess
from typing import Optional, Callable

from ._auto_doc import auto_doc
from ._data_tools import is_valid_data_line
from ._metadata import *
from ._read_lines import read_lines
from ._resources import pkg_path
# from ._version import VERSION

PKG_PATH = pkg_path()
PKG_NAME = PKG_PATH.name

PROJ_DATA = PKG_PATH / 'data'
AUTHOR = (PROJ_DATA / 'author.txt').read_text()
DESCRIPTION = (PROJ_DATA / 'description.txt').read_text()
REQ_FILE = PROJ_DATA / 'requirements.txt'
if not REQ_FILE.exists(): REQ_FILE = PROJ_DATA / 'requirements.in'
if not REQ_FILE.exists(): REQ_FILE.touch()
REQUIREMENTS = '\n'.join([f'* {s}' for s in read_lines(REQ_FILE) if is_valid_data_line(s)])


@auto_doc()
def summarize_docstring(node):
    """Return the first line of a node's docstring, or '' if none."""
    doc = ast.get_docstring(node)
    if not doc:
        return ""
    return doc.strip().splitlines()[0]

@auto_doc()
def build_structure(node):
    """Recursively build a nested dict of class/function structure."""
    structure = {}
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            name = child.name
            summary = summarize_docstring(child)
            # Nested definitions inside
            nested = build_structure(child)
            # Include docstring summary as a special key
            structure[name] = {"__doc__": summary, **nested}
    return structure

@auto_doc()
def module_structure(filepath):
    """Return a nested dict of all classes/functions and their docstring summaries."""
    source = Path(filepath).read_text()
    tree = ast.parse(source, filename=filepath)
    return build_structure(tree)

@auto_doc("Combines auto_doc and automatic function name detection.")
def auto_doc_named(func: Optional[Callable] = None):
    """
        Usage:
            @auto_doc_named
            def my_function(...):
                ...
        
        This will automatically use the function's __name__ for the doc heading.
    """
    if func is None:
        # decorator called with parentheses: @auto_doc_named()
        def wrapper_inner(f):
            f.name = f.__name__
            return auto_doc(f.__name__)(f)
        return wrapper_inner

    # decorator called without parentheses: @auto_doc_named
    return auto_doc(func.__name__)(func)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
