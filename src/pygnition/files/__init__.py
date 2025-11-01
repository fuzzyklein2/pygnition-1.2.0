#!/usr/bin/env python3

from importlib import import_module

from .._auto_doc import auto_class_doc, auto_doc, AUTO_DOC_HEAD
from .._imports import import_chain

PACKAGE_NAME = import_chain()[0]

try:
    _metadata = import_module(f'{PACKAGE_NAME}._metadata')
    globals().update(vars(_metadata))
except ModuleNotFoundError: # Most likely happens in a Jupyter notebook or a console
                            # Appears to happen in pydoc as well.
    from .._metadata import *

__doc__ = f"""The 🔥  pygnition 🔥  package sets up an environment for any script that imports it.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

## Author

{AUTHOR}

## Date

{LAST_SAVED_DATE}

## Usage

```python
from pygnition.program import Program
Program().run()

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.

## [GitHub]({get_upstream_url()})

"""

from .files import File
from .datafile import DataFile
from .textfile import TextFile
from .binaryfile import BinaryFile
from .folders import Folder, WebSiteFolder
from .picklefile import PickleFile
from .jsonfile import JSONFile
from .csvfile import CSVFile
from .imagefile import ImageFile
from .pngfile import PNGFile
from .jpegfile import JPEGFile
from .giffile import GIFFile
from .videofile import VideoFile
from .mp4file import MP4File
from .avifile import AVIFile
from .mkvfile import MKVFile
from .audiofile import AudioFile
from .mp3file import MP3File
from .wavfile import WAVFile
from .flacfile import FLACFile
from .archivefile import ArchiveFile
from .configfile import ConfigFile
from .databasefile import DatabaseFile
from .logfile import LogFile
from .htmlfile import HTMLFile
from .jsfile import JSFile
from .cssfile import CSSFile
from .cgifile import CGIFile
from .scriptfile import ScriptFile
from .executablefile import ExecutableFile
from .specialfile import SpecialFile
from .fifofile import FIFOFile
from .socketfile import SocketFile
from .symlink import SymbolicLink
from .hardlink import HardLink
from .mountpoint import MountPoint
