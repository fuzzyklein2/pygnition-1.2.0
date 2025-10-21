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



# def normalize(s: str) -> str:
#     """Trim and lowercase a string for comparison."""
#     return s.strip().lower()


# def is_affirmative(s: str) -> bool:
#     """Return True if input matches a known affirmative response."""
#     s = normalize(s)
#     return any(s == word or s.startswith(word) for word in AFFIRMATIVES)


# def is_negative(s: str) -> bool:
#     """Return True if input matches a known negative response."""
#     s = normalize(s)
#     return any(s == word or s.startswith(word) for word in NEGATIVES)
    
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

def normalize(s: str) -> str:
    """Trim and lowercase a string for comparison."""
    return s.strip().lower()


def is_affirmative(s: str) -> bool:
    """Return True if input matches a known affirmative response."""
    s = normalize(s)
    return any(s == word or s.startswith(word) for word in AFFIRMATIVES)


def is_negative(s: str) -> bool:
    """Return True if input matches a known negative response."""
    s = normalize(s)
    return any(s == word or s.startswith(word) for word in NEGATIVES)

# def prompt_yes_no(prompt: str, default: str | None = None) -> bool:
#     """
#     Prompt the user for a yes/no answer and return True for yes, False for no.

#     Parameters:
#         prompt: The text to show to the user.
#         default: If provided ("y" or "n"), hitting enter will select this.

#     Returns:
#         True if affirmative, False if negative.
#     """
#     if default:
#         prompt_text = f"{prompt} [{'Y' if default.lower() == 'y' else 'y'}/{'N' if default.lower() == 'n' else 'n'}]: "
#     else:
#         prompt_text = f"{prompt} [y/n]: "

#     while True:
#         reply = input(prompt_text)
#         if not reply and default:
#             reply = default
#         if is_affirmative(reply):
#             return True
#         elif is_negative(reply):
#             return False
#         else:
#             print("Please respond with yes or no.")
