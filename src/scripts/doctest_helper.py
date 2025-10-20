"""
doctest_helper.py — run doctests on modules/packages/folders with flexible matching
"""

import doctest
import importlib
import sys
import pkgutil
from pathlib import Path
import fnmatch

DEFAULT_EXCLUDES = ['*.ipynb', '__pycache__', '*.pyc', '*.pyo', '*.so']

def run_doctests(module_or_path=None, verbose=True, recursive=False, exclude=None):
    """
    Run doctests on a module, package, or folder.

    Parameters:
        module_or_path : str, module object, or Path
            Module name, module object, or folder path. Defaults to current script.
        verbose : bool
            Whether to print full doctest output.
        recursive : bool
            If True, recursively test submodules and subpackages (default: False)
        exclude : list[str] or None
            Additional filename patterns to skip (default: None)

    Returns:
        dict: module name -> (failed, attempted) for each tested module

    Example Usage:

        if __name__ == "__main__":
        from doctest_helper import run_doctests
    
        # Test current package non-recursively, skip extra files
        run_doctests("mypackage", recursive=False, exclude=['*_test.py'])
    
        # Test recursively
        run_doctests("mypackage", recursive=True)

    
    """
    optionflags = (
        doctest.ELLIPSIS |
        doctest.NORMALIZE_WHITESPACE |
        doctest.IGNORE_EXCEPTION_DETAIL
    )

    results = {}
    exclude = exclude or []

    def _should_skip(path: Path):
        patterns = DEFAULT_EXCLUDES + exclude
        return any(fnmatch.fnmatch(path.name, pat) for pat in patterns)

    def _test_module(mod):
        res = doctest.testmod(mod, optionflags=optionflags, verbose=verbose)
        results[mod.__name__] = (res.failed, res.attempted)

    # Determine starting point
    if module_or_path is None:
        module_or_path = Path(sys.argv[0]).stem

    # Convert string paths to modules
    if isinstance(module_or_path, Path):
        module_or_path = str(module_or_path)
    if isinstance(module_or_path, str):
        try:
            mod = importlib.import_module(module_or_path)
        except ModuleNotFoundError:
            mod = None

    # Single module
    if 'mod' in locals() and mod is not None:
        _test_module(mod)
        if recursive and hasattr(mod, '__path__'):
            for finder, name, ispkg in pkgutil.walk_packages(mod.__path__, mod.__name__ + "."):
                submod = importlib.import_module(name)
                _test_module(submod)
    else:
        # Treat as folder path
        folder = Path(module_or_path).resolve()
        sys.path.insert(0, str(folder.parent))
        if recursive:
            pyfiles = folder.rglob("*.py")
        else:
            pyfiles = folder.glob("*.py")

        for pyfile in pyfiles:
            if _should_skip(pyfile):
                continue
            modname = ".".join(pyfile.with_suffix("").relative_to(folder.parent).parts)
            submod = importlib.import_module(modname)
            _test_module(submod)

    # Summary
    for name, (failed, attempted) in results.items():
        if failed == 0:
            print(f"✅ All doctests passed for {name}")
        else:
            print(f"❌ {failed}/{attempted} doctests failed in {name}")

    return results

