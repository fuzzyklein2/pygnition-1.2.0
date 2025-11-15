#!/usr/bin/env python3

from pathlib import Path

from pygnition import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {__package__}.{MODULE_NAME}
Version: 1.2.0
Author: Fuzzy Klein
Date: 2025-11-03

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

## [GitHub](https://github.com/fuzzyklein2/pygnition-1.2.0/)

"""

def is_valid_data_line(s:str   # Should be a line from a configuration file of some sort.
                      )->bool: # True if the line does not start with a comment.
                               # Other criteria should probably be involved as well.
    """
        Return True if the line does not begin with a comment
        and False if it does

        ### Example Usage

        >>> is_valid_data_line("# starts with comment")
        False

        >>> is_valid_data_line("anything else")
        True
    """
    if s.startswith('#') or s.isspace() or not s: return False
    return True

def get_data(p: Path, # This must be the application data path `root/src/app/data`.
             s: str   # The stem of the desired filename.
            ) -> str: # The contents of the file `root/src/<app_name>/`s`.txt.
    """ Get the contents of the file p / s.txt """
    data_file = p / f'{s}.txt'
    try:
        return data_file.read_text()
    except FileNotFoundError:
        return ''

if __name__ == '__main__':
    print(f'Testing {__file__}')
    import doctest
    doctest.testmod()
    print(f'{__file__} execution complete.')
    