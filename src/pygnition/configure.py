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

from configparser import ConfigParser as CP
from pathlib import Path

from .arguments import parse_arguments
from .constants import NEWLINE
from .picts import WARNING_PICT
from .stdinput import get_piped_input
from .where import USER_PREFS_DIR

def config(p:str|Path)->dict:
    """ Simple function to just read a `*.cfg` file with no sections. """
    p = Path(p)
    lines = read_lines(p)
    d = dict()
    for l in lines:
        k, _, v = l.partition('=')
        v = v.partition('#')[0]
        d[k.strip()] = v.strip()
    return d

class Configuration():
    def __init__(self, files:list):
        # Normalize files into a list of strings
        if files is None:
            files_list = []
        elif isinstance(files, (str, Path)):
            files_list = [str(files)]
        elif isinstance(files, list):
            files_list = [str(f) for f in files]
        else:
            raise TypeError(f"files must be str, Path, or list of str/Path, got {type(files)}")

        self.config = CP()
        if files_list:
            for f in files_list:
                try:
                    lines = Path(f).read_text().splitlines()
                except FileNotFoundError:
                    print(f'{WARNING_PICT}Configuration file not found: {f}')
                    break
                if not lines[0].startswith('DEFAULT'):
                    lines.insert(0, '[DEFAULT]')
                self.config.read_string(NEWLINE.join(lines))
            # self.config.read(files)

    def as_dict(self) -> dict:
        result = {'DEFAULT': dict(self.config.defaults())}
        result.update({section: dict(self.config[section]) for section in self.config.sections()})
        return result

def configure(files:list|None=None):
    # rp(f"{DEBUG_PICT}[hot_pink2][bold]`configure`[/bold][/hot_pink2]")
    # breakpoint()
    if not files:
        files = list()
    # else: print(f'{type(files)=}')
    config = Configuration(files)
#     print(f'''Configuration:

# {pformat(config.as_dict())}
# ''')
    return Configuration(files)
    
@auto_doc()
def get_user_pref(name: str # Key name to look for in the config file.
                 ) -> str:  # Everything after the '=' and before any '#' if a matching line is
                            # found. `''` if no match is found, or maybe `None`.
    """ Read the file at `Path.home() / ('.' + PACKAGE_NAME) / 'config.ini') and look for a
        value to match the given key.
    """
    PREFS_FILE = USER_PREFS_DIR / 'prefs.cfg'
    prefs = config(PREFS_FILE)
    try:
        return prefs[name]
    except KeyError:
        return None
    
if __name__ == '__main__':
    from pprint import pprint as pp
    
    # from .interpreters import PROJECT_NAME
    
    print(f'Running {__file__}')
    # print(f'Program path: {PROGRAM_PATH}')
    # print("Running `configure.py` ...")
    config = configure(USER_PREFS_DIR / 'config.ini')
    pp(config.as_dict())

