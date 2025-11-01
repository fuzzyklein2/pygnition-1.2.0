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

import logging
import os
from pathlib import Path
from pprint import pformat
import shutil
from types import SimpleNamespace

from pygnition.arguments import parse_arguments
from pygnition.configure import configure
# from pygnition.constants import DESCRIPTION, EPILOG, VERSION
from pygnition.environment import Environment
from .interpreters import RUNNING_CLI, RUNNING_GATEWAY
from pygnition.lumberjack import debug, error, info, setuplog, stop, warn
from pygnition.stdinput import get_piped_input
from pygnition.tools import mkdir
from .where import DEBUG, PROJ_DATA, TESTING, USER_DATA_DIR, USER_PREFS_DIR, VERBOSE

# breakpoint()
INPUT = get_piped_input()

# PROJECT_DIR = Path(__file__).resolve().parent.parent if RUNNING_CLI else Path(os.curdir).resolve()
ARGS_FILE = PROJ_DATA / 'std_opts.csv'
# CONFIG_FILE = USER_DATA_DIR / f'etc/{PROGRAM_NAME}.cfg'
# if not CONFIG_FILE.exists():

# CONFIG_FILE = PROJECT_DIR / 'etc/config.ini'
# LOG_FILE = PROJECT_DIR / f'logs/{PROGRAM_NAME}.log'
if not USER_PREFS_DIR.exists():
    shutil.copytree(PACKAGE_PATH / 'etc', USER_PREFS_DIR)
CONFIG_FILES = [USER_PREFS_DIR / s for s in os.listdir(USER_PREFS_DIR) if Path(s).suffix in {'.ini', '.cfg'}]

LOG_FILE = USER_DATA_DIR / f'logs/{PACKAGE_NAME}.log'

# assert(PROJECT_DIR.exists())
# assert(ARGS_FILE.exists())
# assert(CONFIG_FILE.exists())

ARGS = None
if RUNNING_CLI:
    # print(f'Arguments file: {ARGS_FILE}')
    if ARGS_FILE.exists():
        ARGS = parse_arguments(ARGS_FILE, PACKAGE_NAME, VERSION, DESCRIPTION,
                               (PROJ_DATA / 'epilog.txt').read_text().strip())

# print(str(ARGS_FILE))

# assert(ARGS)

if ARGS:
    if hasattr(ARGS, 'config'):
        if ARGS.config:
            CONFIG_FILES = [ARGS.config]

ENV = Environment()

# print('Configuration file: ' + str(CONFIG_FILE))
CONFIG = None
if CONFIG_FILES:
    CONFIG = configure(CONFIG_FILES).config
#else:
#    if not USER_PREFS_DIR.exists():
#        shutil.copytree(PROJECT_DIR / 'etc', USER_PREFS_DIR)
#
if ARGS:
    if hasattr(ARGS, 'log'):
        if ARGS.log:
            LOG_FILE = ARGS.log
elif CONFIG and ('LOG_FILE' in CONFIG['DEFAULT'].keys()):
    LOG_FILE = CONFIG['DEFAULT']['LOG_FILE']
# LOG_FILE = ARGS.LOG_FILE if ARGS.LOG_FILE else CONFIG['DEFAULT']['LOG_FILE']

# print(f'{ARGS=}')

LOG_LEVEL = logging.WARNING

if ARGS:
    if ARGS.debug or ARGS.testing:
        LOG_LEVEL = logging.DEBUG
    elif ARGS.verbose:
        LOG_LEVEL = logging.INFO

# print(f'{LOG_FILE=}\n{LOG_LEVEL=}')

if LOG_FILE.parent.exists():
    setuplog(LOG_FILE, LOG_LEVEL)

SETTINGS = dict()
if CONFIG: SETTINGS.update(dict(CONFIG['DEFAULT']))
if ENV: SETTINGS.update(ENV)
if ARGS: SETTINGS.update(vars(ARGS))
if INPUT: SETTINGS.update({'input', INPUT})



class Settings(SimpleNamespace):
    def __init__(self, *args, **kwargs):
        super().__init__(**SETTINGS)
        self.config_files = CONFIG_FILES
        if TESTING: self.debug = True
        else: self.debug = DEBUG
        if self.debug: self.verbose = True
        else: self.verbose = VERBOSE

    def dumps(self):
        d = {k: v for k, v in vars(ARGS).items() if k != 'args'} if ARGS else 'None'
        return f'''
Command line options:
{pformat(d)}

Command line arguments:
{pformat(self.args) if ARGS else 'None'}

    Defined in {ARGS_FILE}

Environment variables:
{ENV.dumps()}

Configuration files:
{pformat(self.config_files)}

Configuration:
{pformat(dict(CONFIG['DEFAULT']) if CONFIG else 'WARNING! Configuration file does not exist!')}'''

    def dump(self):
        if RUNNING_GATEWAY:
            pass
        else:
            debug(f"""{self.__class__.__name__} settings:
{self.dumps()}
""")
    
if __name__ == '__main__':
    debug(f'Running {PACKAGE_NAME}')
    debug(f'{type(ARGS)=}')
    debug(f'{dict(CONFIG['DEFAULT'])=}')
    debug(f'''Settings:
{pformat(Settings())}
''')
    # s = Settings()
    # debug(f'{s.debug=}')
    # debug(f'{s.input=}')
    # debug(f'{s.args=}')
    # debug(f'{dict(s.config[s.section]=}')
    # debug(f'{s.logfile=}')
    
