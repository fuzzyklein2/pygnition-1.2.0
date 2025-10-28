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

from pathlib import Path
from pprint import pformat

from rich import print as rp

from .files.files import is_hidden, is_visible
from .lumberjack import debug, error, info, stop, warn 
from .picts import DEBUG_PICT, FOLDER_PICT, GEAR_PICT, LINK_PICT
from .program import Program, PROGRAM_NAME

class Filter(Program):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paths = [Path(f) for f in self.args]
        if self.testing: print(f"""{DEBUG_PICT} Filter Paths:

{pformat(self.paths)}
""")

    def process_directory(self, p:Path):
        if self.recursive:
            if self.verbose: print(f'{FOLDER_PICT}Processing directory: {str(p)} ...')
            for f in [Path(s) for s in p.rglob('*') if is_visible(s) or self.all]:
                self.process_path(Path(f))
        else:
            if self.verbose: print(f'{FOLDER_PICT}Skipping directory: {str(p)} ...')

    def process_file(self, p:Path):
        if self.verbose: print(f'Processing {str(p)} ...')

    def process_path(self, p:Path):
        if self.verbose: print(f"{GEAR_PICT}Processing {str(p)} ...")
            
        if not p.exists():
            warn(f"File {str(p)} does not exist!")
            return
            
        if is_hidden(p) and not self.all:
            if self.verbose:
                print(f'Skipping {str(p)} ...')
            return

        if p.is_block_device():
            info(f'Skipping block device: {p.name}')

        if p.is_char_device():
            info(f'Skipping char device: {p.name}')

        if p.is_fifo():
            info(f'Skipping fifo: {p.name}')

        if p.is_mount():
            info(f'Skipping mount: {p.name}')

        if p.is_socket():
            info(f'Skipping socket: {p.name}')
        
        if p.is_symlink():
            target = p.readlink()
            output = 'symbolic link '
            exists = target.exists()
            color = 'cyan' if exists else 'red'
            output += f' --> [{color} bold] '
            output += str(target)
            output += f'[/{color} bold]'
            if self.follow:
                rp(f'{LINK_PICT}Processing {output}')
                rp(f'{GEAR_PICT}Processing target [cyan][bold]{str(target.resolve())}')
            else:
                rp(f'{LINK_PICT}Skipping symbolic link {output}')
            return
                
        if p.is_dir():
            self.process_directory(p)

        self.process_file(p)


    def run(self):
        # super().run()
        if self.verbose: print(f"{GEAR_PICT}Processing files ...")

        for p in self.paths:
            self.process_path(p)
            
        # print(f"{STOP_PICT}Execution complete.")

if __name__ == '__main__':
    print(type(is_visible))
    f = Filter()
    if f.testing:
        info(f'Running {PROGRAM_NAME} ...')
        debug(f'Command line arguments:\n\n{pformat(f.args)}\n')
    Filter().run()
    # print(RECURSIVE)
    