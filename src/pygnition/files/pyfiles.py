#!/usr/bin/env python3

from pathlib import Path

from ..startmeup import *

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

from functools import partial
from pathlib import Path

from ..gui_tools import choose_file
from ..lumberjack import debug, error, info, stop, warn
from ..tools import cd, cwd, run_cmd
from ..where import cwd_mover

from .files import File
from .textfiles import SrcFile

pick_file = partial(choose_file,
                    initial_path=Path(f'src/{PACKAGE_NAME}/'),
                    filters=[('Python file', '*.py')]
                   ) # Chooses a Python file

# Python files
@File.register_ext(".py")
class PyFile(SrcFile):
    def pick(self):
        """ Prompt the user to choose a Python `*.py` file. """
        self.path = choose_file(
            initial_path=cwd(),
            filters=[('Python file', '*.py')]
        )
        if self.path:
            info(f'User chose {self.path}')
        else:
            info("User cancelled.")

    def is_in_package(self) -> bool:
        return (self.path.parent / '__init__.py').exists()

    @cwd_mover()
    def run(self) -> subprocess.CompletedProcess | None:
        if not self.path: 
            self.pick()
        if not self.path:
            return None

        if self.is_in_package():
            debug(f'File {str(self.path)} is in a package folder.')
            cd(self.path.parent.parent)
            debug(f'Changed to directory {cwd()}')
            process = run_cmd([
                sys.executable,
                '-m',
                f'{self.path.parent.name}.{self.path.stem}'
            ])
        else:
            process = run_cmd([sys.executable, str(self.path)])

        cd(self.run._CWD)
        debug(f'Changed back to {cwd()}')
        return process
