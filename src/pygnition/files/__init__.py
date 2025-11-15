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

from pygnition.files.files import File
from pygnition.files.pyfiles import PyFile

from pygnition.files.datafile import DataFile
from pygnition.files.textfile import TextFile
from pygnition.files.binaryfile import BinaryFile
from pygnition.files.folders import Folder, WebSiteFolder
from pygnition.files.picklefile import PickleFile
from pygnition.files.jsonfile import JSONFile
from pygnition.files.csvfile import CSVFile
from pygnition.files.imagefile import ImageFile
from pygnition.files.pngfile import PNGFile
from pygnition.files.jpegfile import JPEGFile
from pygnition.files.giffile import GIFFile
from pygnition.files.videofile import VideoFile
from pygnition.files.mp4file import MP4File
from pygnition.files.avifile import AVIFile
from pygnition.files.mkvfile import MKVFile
from pygnition.files.audiofile import AudioFile
from pygnition.files.mp3file import MP3File
from pygnition.files.wavfile import WAVFile
from pygnition.files.flacfile import FLACFile
from pygnition.files.archivefile import ArchiveFile
from pygnition.files.configfile import ConfigFile
from pygnition.files.databasefile import DatabaseFile
from pygnition.files.logfile import LogFile
from pygnition.files.htmlfile import HTMLFile
from pygnition.files.jsfile import JSFile
from pygnition.files.cssfile import CSSFile
from pygnition.files.cgifile import CGIFile
from pygnition.files.scriptfile import ScriptFile
from pygnition.files.executablefile import ExecutableFile
from pygnition.files.specialfile import SpecialFile
from pygnition.files.fifofile import FIFOFile
from pygnition.files.socketfile import SocketFile
from pygnition.files.symlink import SymbolicLink
from pygnition.files.hardlink import HardLink
from pygnition.files.mountpoint import MountPoint
