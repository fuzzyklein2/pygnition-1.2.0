# #!/usr/bin/env python3

# from pathlib import Path

# from .startmeup import *

# MODULE_NAME = Path(__file__).stem

# __doc__ = f"""Python IDE for the command line.

# ========== ⚠️ WARNING! ⚠️ ==========
# This project is currently under construction.
# Stay tuned for updates.

# Module: {PROJECT_NAME}.{MODULE_NAME}
# Version: {VERSION}
# Author: {AUTHOR}
# Date: {str(last_saved_datetime(__file__).date()).split('.')[0]}

# ## Description

# This module defines the Workshop class.

# ## Typical Use
# ```python
# app = Workshop()
# app.run()

# Notes
# -----
# You can include implementation notes, dependencies, or version-specific
# details here.

# """

from importlib import import_module, resources
import inspect
import os
from pathlib import Path
import runpy
import sys
import traceback

def import_chain():
    stack = inspect.stack()
    chain = []

    for frame_info in stack:
        filename = frame_info.filename

        # Skip frames from Python internals or this module itself
        if filename.startswith("<") or filename == __file__:
            continue

        # Try to map filename back to a module/package name
        module_name = None
        for name, module in sys.modules.items():
            if hasattr(module, '__file__') and module.__file__:
                if os.path.abspath(module.__file__) == os.path.abspath(filename):
                    module_name = name
                    break
        if module_name is None:
            module_name = os.path.splitext(os.path.basename(filename))[0]

        chain.append(module_name)

    return chain[::-1]  # reverse to show import order from root

# Print import chain at import time
# print(f"{__name__} imported via chain: {import_chain()}")

def pkg_path(name:str) -> Path:
    """
    Return the root path of this installed package.
    Raises RuntimeError if the package is not importable.
    """

    # --- Verify package is importable ---
    try:
        __import__(name)
    except ImportError:
        raise RuntimeError(
            f"Package '{name}' is not importable. "
            "Make sure it’s installed (e.g. `pip install -e .`) "
            "and available in this environment."
        )

    # --- Return the installed package root ---
    return Path(resources.files(name))

def safe_import_module(module_name: str, project_dir: Path) -> Tuple[Optional[Union[ModuleType, dict]], Optional[str]]:
    try:
        mod = import_module(module_name)
        return mod, None
    except Exception:
        first_tb = traceback.format_exc()
    try:
        module_globals = runpy.run_module(module_name, run_name=module_name, alter_sys=True)
        return module_globals, None
    except Exception:
        second_tb = traceback.format_exc()
        combined = f"Import attempt using importlib.import_module failed:\n\n{first_tb}\n\n" \
                   f"Fallback attempt using runpy.run_module failed:\n\n{second_tb}"
        return None, combined

