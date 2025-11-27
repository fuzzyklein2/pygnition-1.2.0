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

import keyword
import re

def is_valid_module_name(name: str) -> bool:
    return name.isidentifier() and not keyword.iskeyword(name)

def slugify(text: str) -> str:
    """
    Convert a string into a URL-friendly “slug”.

    Steps:
    - Lowercase the text.
    - Remove all characters except word characters, whitespace, and hyphens.
    - Replace spaces with hyphens.

    Parameters
    ----------
    text : str
        The input string to convert.

    Returns
    -------
    str
        A sanitized, hyphen-separated slug suitable for filenames or URLs.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = text.replace(" ", "-")
    return text
