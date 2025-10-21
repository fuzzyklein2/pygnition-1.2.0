#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PROJECT_NAME}.{MODULE_NAME}
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


from datetime import datetime
import sys

from .interpreters import RUNNING_CLI
from .picts import CRITICAL_PICT, current_clock_pict, DEBUG_PICT, ERROR_PICT, GEAR_PICT, INFO_PICT, LOG_PICT, WARNING_PICT
from .tools import *
from .where import USER_DATA_DIR, VERBOSE

LOG_PICTS = { logging.DEBUG: DEBUG_PICT,
              logging.INFO: INFO_PICT,
              logging.WARNING: WARNING_PICT,
              logging.ERROR: ERROR_PICT,
              logging.CRITICAL: CRITICAL_PICT
            }

@auto_doc("Set up the logging module and file.")
def setuplog(LOGFILE:Path|str, level):
    if type(LOGFILE) is str:
        LOGFILE = Path(LOGFILE)
        
    if LOGFILE.exists():
        LOGFILE.write_text('')
    else:
        LOGFILE.parent.mkdir(parents=True, exist_ok=True)
        
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter('%(message)s')
    # formatter = logging.Formatter(f'{LOG_PICTS
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOGFILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug(f"{GEAR_PICT}Logging configuration complete.")
    logger.debug(f'{LOG_PICT}Log file: {LOGFILE.resolve()}')
    now = datetime.now()
    logger.debug(f'{current_clock_pict(now)}Current time: {now}')

    return logger

def log(level, message):
    if NEWLINE in message:
        logging.log(level, '')
    logging.log(level, f"{LOG_PICTS[level]}{message}")
    # if NEWLINE in message:
    #     logging.log(level, '')

def debug(message):
    log(logging.DEBUG, message)

def info(message):
    log(logging.INFO, message)

def warn(message):
    log(logging.WARNING, message)

def error(message):
    log(logging.ERROR, message)

def stop(message):
    log(logging.CRITICAL, message)
    if RUNNING_CLI:
        exit(1)

if __name__ == '__main__':
    setuplog(USER_DATA_DIR / f'logs/{PROJECT_NAME}.log',
             level=logging.DEBUG)
    debug(f'Testing {PROJECT_NAME}')