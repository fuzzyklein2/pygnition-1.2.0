#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️ WARNING! ⚠️ ==========
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
app = Workshop()
app.run()

Notes
-----
You can include implementation notes, dependencies, or version-specific
details here.

"""



from pathlib import Path
# if __package__:
#     from .utils import *
# else:
#     from utils import *

from pygnition.utils import get_docstring_from_file, grep, remove_tag
from pygnition.where import PROGRAM_NAME, PROGRAM_PATH

NEWLINE = '\n'
HYPHEN = '-'

# RUNNING_IN_JUPYTER = Path(sys.argv[0]).stem.startswith('ipykernel')
# RUNNING_CLI = not RUNNING_IN_JUPYTER
# NOTEBOOK = 'notebook'

FILE_TAG = '@file'
BRIEF_TAG = '@brief'
VERSION_TAG = '@version'

PROGRAM = PROGRAM_NAME
VERSION = None
MAIN_FILE = PROGRAM_PATH

# TODO: This stretch should be revised to parse the new-style docstrings,
#       or just get the version from PROJECT_PATH.
try:
    DOCSTR = get_docstring_from_file(MAIN_FILE)
    DOCSTR_MISSING = not bool(DOCSTR)
except (FileNotFoundError, TypeError, IsADirectoryError) as e:
    # print(f'{WARNING_PICT} File not found: {MAIN_FILE}')
    DOCSTR_MISSING = True
    
if DOCSTR_MISSING:
    VERSION = '1.0.0'
    DESCRIPTION = f'Python script: {MAIN_FILE}'
    EPILOG = 'https://github.com/fuzzyklein2/workshop-0.0.1b'
else:
    VERSION = remove_tag(grep(VERSION_TAG, DOCSTR)[0])
    DESCRIPTION = remove_tag(grep(BRIEF_TAG, DOCSTR)[0])
    EPILOG = DOCSTR[-1]

CWD = Path.cwd()

if __name__ == '__main__':
    pass
