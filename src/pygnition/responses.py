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

AFFIRMATIVES = [
    "y",
    "yes",
    "yep",
    "yup",
    "yea",
    "yeah",
    "affirmative",
    "sure",
    "indeed",
    "absolutely",
    "certainly",
    "of course",
    "ok",
    "okay",
    "alright",
    "roger",
    "naturally",
    "definitely",
    "fine",
    "correct",
    "exactly",
    "totally",
    "cool"
]

NEGATIVES = [
    "n",
    "no",
    "nope",
    "nah",
    "nay",
    "never",
    "negative",
    "not",
    "incorrect",
    "wrong",
    "none",
    "refuse",
    "decline",
    "cannot",
    "impossible",
    "disagree",
    "stop"
]

@auto_doc(AUTO_DOC_HEAD)
def normalize(s: str) -> str:
    """Trim and lowercase a string for comparison."""
    return s.strip().lower()


@auto_doc(AUTO_DOC_HEAD)
def is_affirmative(s: str) -> bool:
    """Return True if input matches a known affirmative response."""
    s = normalize(s)
    return any(s == word or s.startswith(word) for word in AFFIRMATIVES)


@auto_doc(AUTO_DOC_HEAD)
def is_negative(s: str) -> bool:
    """Return True if input matches a known negative response."""
    s = normalize(s)
    return any(s == word or s.startswith(word) for word in NEGATIVES)

if __name__ == '__main__':
    print(f'Running {__file__}')