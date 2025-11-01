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

from .datafile import DataFile
from .binaryfile import BinaryFile

class PickleFile(DataFile, BinaryFile):
    '''
import json
import pickle
from pathlib import Path

def json_to_pickle(json_path: str | Path, pickle_path: str | Path):
    """Load a JSON file and save it as a pickle file."""
    json_path = Path(json_path)
    pickle_path = Path(pickle_path)

    # Load the JSON data
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Dump it as a pickle
    with pickle_path.open("wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Converted {json_path} → {pickle_path}")

# Example usage:
json_to_pickle("emojis.json", "emoji_subset.pkl")

    '''
    