#!/usr/bin/env python3

from pathlib import Path

MODULE_NAME = Path(__file__).stem

from datetime import datetime
from importlib import resources
from pathlib import Path
import subprocess
import sys

from ._data_tools import is_valid_data_line
from ._imports import pkg_path
from ._last_saved_date import last_saved_datetime
from ._read_lines import read_lines

PROJECT_NAME = "pygnition"  # your package name

# def pkg_path() -> Path:
#     """
#     Return the root path of this installed package.
#     Raises RuntimeError if the package is not importable.
#     """
#     # Detect Jupyter (just for reference, though it's not critical anymore)
#     def in_jupyter() -> bool:
#         try:
#             from IPython import get_ipython
#             return get_ipython() is not None
#         except Exception:
#             return False

#     # --- Verify package is importable ---
#     try:
#         __import__(PROJECT_NAME)
#     except ImportError:
#         raise RuntimeError(
#             f"Package '{PROJECT_NAME}' is not importable. "
#             "Make sure it’s installed (e.g. `pip install -e .`) "
#             "and available in this environment."
#         )

#     # --- Return the installed package root ---
#     return Path(resources.files(PROJECT_NAME))

# def pkg_path() -> Path
#     if INTERPETER == Interpreters.JUPYTER:
        
#     if __package__: return resources.files(f'{PROJECT_NAME}')
#     else: return Path(__file__).parent

PACKAGE_PATH = pkg_path(PROJECT_NAME)
VERSION = '1.2.0b'
AUTHOR = 'Russell Klein'

# def git_repo_last_commit_datetime() -> datetime | None:
#     try:
#         result = subprocess.run(
#             ["git", "log", "-1", "--format=%ct"],
#             capture_output=True, text=True, check=True
#         )
#         timestamp = int(result.stdout.strip())
#         return datetime.fromtimestamp(timestamp)
#     except subprocess.CalledProcessError:
#         return None

# def last_saved_datetime(path: str | Path, repo_wide: bool = False) -> datetime | None:
#     """
#     Return the datetime of the last Git commit for a file or repo.
#     Falls back to filesystem modification time if not committed yet.

#     :param path: Path to file or directory.
#     :param repo_wide: If True, use the latest commit in the repo.
#     :return: datetime object or None if unavailable.
#     """
#     path = Path(path).resolve()

#     # --- 1. Try git commit timestamp ---
#     try:
#         args = ["git", "log", "-1", "--format=%ct"]
#         if not repo_wide:
#             args.append(str(path))
#         result = subprocess.run(args, capture_output=True, text=True, check=True)
#         ts = result.stdout.strip()
#         if ts:
#             return datetime.fromtimestamp(int(ts))
#     except subprocess.CalledProcessError:
#         pass  # not in git or not committed

#     # --- 2. Fall back to file modification time ---
#     try:
#         return datetime.fromtimestamp(path.stat().st_mtime)
#     except FileNotFoundError:
#         return None

LAST_SAVED_DATE = last_saved_datetime(__file__).date()
PROJECT_DATA_DIR = PACKAGE_PATH / 'data'
DESCRIPTION = (PROJECT_DATA_DIR / 'description.txt').read_text()
REQ_FILE = PROJECT_DATA_DIR / 'requirements.txt'
if not REQ_FILE.exists(): REQ_FILE = PROJECT_DATA_DIR / 'requirements.in'
if not REQ_FILE.exists(): REQ_FILE.touch()
REQUIREMENTS = '\n'.join([f'* {s}' for s in read_lines(REQ_FILE) if is_valid_data_line(s)])

__doc__ = f"""Provides metadata for the project, notably the `PROJECT_NAME`.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Package: 🔥  pygnition 🔥
Module: {MODULE_NAME}
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

