#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
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
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

"""

from argparse import ArgumentParser as AP
from collections import namedtuple
import csv
import sys

# import pandas as pd

from .where import PROGRAM_NAME

EPILOG = (PROJ_DATA / 'epilog.txt').read_text()

@auto_doc("Look for options and arguments in a CSV file.")
def get_args(p:Path|str)->list[list[list|dict]]|None:
    """
        Sample code from ChatGPT:

        import csv
        from collections import namedtuple
        
        # Open the CSV file
        with open("data.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # reads each row as a dict
            # Create a namedtuple class dynamically from fieldnames
            Row = namedtuple("Row", reader.fieldnames)
            
            # Convert each row dict to a namedtuple
            rows = [Row(**row) for row in reader]
        
        # Example usage
        for r in rows:
            print(r.name, r.age, r.city)

    """
    if type(p) is str: p = Path(p)

    if p.suffix == '.pkl':
        with open(p, 'rb') as f:  # 'rb' = read binary
            return pickle.load(f)

    result = list()
    with open(p, newline='') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        Row = namedtuple("Row", columns)
        rows = [Row(**row) for row in reader]
        for r in rows:
            L = list()
            L2 = list()
            if r.short: L2.append(r.short)
            if r.long:  L2.append(r.long)
            L.append(L2)
            D = dict()
            for s in columns[2:]:
                value = getattr(r, s)
                if value:
                    D[s] = value
            L.append(D)
            result.append(L)
    return result

@auto_doc()
def parse_arguments(arg_file:Path|str,
                    program_name:str,
                    program_version:str,
                    description:str,
                    epilog:str):
    STD_OPTS = get_args(arg_file)
    STD_OPTS.append([["-V", "--version"],
                     {"action": "version",
                      "version": f"{program_name} {program_version}",
                      "help": "Display the program name and version, then exit."}])


    ap = AP(prog=program_name, description=description, epilog=epilog)
    for option in STD_OPTS:
        ap.add_argument(*option[0], **option[1])

    return ap.parse_args(sys.argv[1:])

class Arguments():
    def __init__(self):
        self._data = ARGS

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, ns):
        self._data = ns

    @data.deleter
    def data(self):
        del self._data

if __name__ == '__main__':
    from pprint import pprint as pp
    ARGS_CSV_FILE = PROJ_DATA / 'std_opts.csv'
    ARGS = parse_arguments(ARGS_CSV_FILE,
                           PROGRAM_NAME,
                           VERSION,
                           DESCRIPTION,
                           EPILOG)
    pp(ARGS.__dict__)

    # ARGS = parse_arguments(CMD_LINE_ARGS_FILE,
    #                        PROGRAM, VERSION,
    #                        DESCRIPTION, EPILOG)

