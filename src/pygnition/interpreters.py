from enum import auto, Enum
import os
from pathlib import Path
import sys

from ._imports import import_chain

class Interpreters(Enum):
    IPYTHON = auto()
    CONSOLE = auto()
    JUPYTER = auto()
    CLI = auto()
    GATEWAY = auto()
    TKINTER = auto()
    UNKNOWN = auto()

from .lists import first_after_last_digits

# ---------------------------
# Program environment
# ---------------------------
RUNNING_CLI = False
RUNNING_CONSOLE = False
RUNNING_IN_JUPYTER = False
RUNNING_GATEWAY = False

# ---------------------------
# Runtime options
# ---------------------------
DEBUG = False
VERBOSE = False
WARNINGS = False
TESTING = False

# ---------------------------
# Program variables
# ---------------------------
PROGRAM_NAME = "UNKNOWN"
PROGRAM_PATH = None
CALLING_MODULE = None

# ---------------------------
# Determine interpreter
# ---------------------------
CALLERS = import_chain()

if not sys.argv[0]: # Running console
    RUNNING_CONSOLE = True
    INTERPRETER = Interpreters.CONSOLE
    CALLING_MODULE = None

if "GATEWAY_INTERFACE" in os.environ: # Maybe, maybe not. CGI :/
    RUNNING_GATEWAY = True
    INTERPRETER = Interpreters.GATEWAY
    CALLING_MODULE = '__main__'

elif "ipykernel" in sys.modules: # Jupyter Lab
    RUNNING_IN_JUPYTER = True
    INTERPRETER = Interpreters.JUPYTER
    CALLING_MODULE = first_after_last_digits(CALLERS)

elif "IPython" in sys.modules: # ipython
    RUNNING_CONSOLE = True
    INTERPRETER = Interpreters.IPYTHON
    CALLING_MODULE = list(filter(lambda s: not (s.startswith('IPython') or s.startswith('traitlets') or s == 'ipython3'), CALLERS))[0]

elif sys.stdin.isatty(): # CLI
    if not RUNNING_CONSOLE:
        RUNNING_CLI = True
        # RUNNING_CONSOLE = True
        INTERPRETER = Interpreters.CLI
        CALLING_MODULE = '__main__'
        
else:
    # fallback
    RUNNING_CLI = True
    INTERPRETER = Interpreters.UNKNOWN

if CALLING_MODULE:
    try:
        PROGRAM_PATH = Path(sys.modules[CALLING_MODULE].__file__).resolve()
    except (KeyError, AttributeError):
        # Running in interactive console or notebook
        PROGRAM_PATH = None

# if not PROGRAM_PATH:
#     PROJECT_DIR = Path.cwd()
# else:
#     PROJECT_DIR = PROGRAM_PATH.parent.parent.parent

# if RUNNING_CLI or RUNNING_GATEWAY:
#     PROJECT_DIR = PROJECT_DIR.parent

# PROGRAM_NAME = PROJECT_DIR.stem.split('-')[0]

# ---------------------------
# Project and user directories
# ---------------------------
# PROJECT_NAME = PROGRAM_NAME
