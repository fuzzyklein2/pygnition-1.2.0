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


class List:
    pass

@auto_doc()
def first_after_last_digits(strings: list[str]) -> str | None:
    """
        Return the `str` directly after the last `str` containing only digits
        in `strings`.
    """
    last_digit_index = None
    for i, s in enumerate(strings):
        if s.isdigit():
            last_digit_index = i
    if last_digit_index is not None and last_digit_index + 1 < len(strings):
        return strings[last_digit_index + 1]
    return None

class List(list):
    """Add some functions from the C++ STL list<type> class to the Python list."""
    def replace(self, old, new, *, all=False, in_place=True):
        """
        Replace the first or all occurrences of `old` with `new`.

        Args:
            old: The element to replace.
            new: The new element to insert.
            all (bool, optional): If True, replace *all* occurrences; otherwise only the first. Default is False.
            in_place (bool, optional): If True, modify this List in place; otherwise, return a new List. Default is True.

        Returns:
            self if in_place is True, otherwise a new List with replacements applied.

        Example Usage:

            >>> l1 = List([1, 2, 3, 4])
            >>> old = 3
            >>> new = 7
            >>> l1.replace(old, new)
            [1, 2, 7, 4]
            >>> l1
            [1, 2, 6, 4]
            >>> l1.replace(2, 28, in_place=False)
            [1, 28, 7, 4]
            >>> l1
            [1, 2, 7, 4]
            
        """
        target = self if in_place else self.copy()

        try:
            idx = target.index(old)
        except ValueError:
            return target

        target[idx] = new

        if all:
            # Replace all subsequent occurrences
            next_index = idx + 1
            while True:
                try:
                    idx = target.index(old, next_index)
                    target[idx] = new
                    next_index = idx + 1
                except ValueError:
                    break

        return target

    @auto_doc("Erase the given elements from the list, in place or otherwise.")
    def erase(*args:int|slice|tuple|range, in_place=True, )->List:
        pass
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()