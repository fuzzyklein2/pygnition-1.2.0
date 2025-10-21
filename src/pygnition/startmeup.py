#!/usr/bin/env python3

# from pathlib import Path

# from .startmeup import *

# MODULE_NAME = Path(__file__).stem

# __doc__ = f"""Python IDE for the command line.

# ========== ⚠️  WARNING! ⚠️  ==========
# This project is currently under construction.
# Stay tuned for updates.

# Module: {PROJECT_NAME}.{MODULE_NAME}
# Version: {VERSION}
# Author: {AUTHOR}
# Date: {LAST_SAVED_DATE}

# ## Description

# This module defines the Workshop class.

# ## Typical Use
# ```python
# args = parse_arguments()

# ## Notes

# You can include implementation notes, dependencies, or version-specific
# details here.

# """


from importlib import import_module

# Import everything from the current package's __init__.py
if __package__:
    globals().update(import_module(__package__).__dict__)
else:
    # Fallback for running directly without the -m flag
    from __init__ import *

