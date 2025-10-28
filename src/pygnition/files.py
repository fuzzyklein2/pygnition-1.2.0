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

from functools import partial
import getpass
from io import StringIO
import mimetypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import magic
from rich import print as rp

# from ._metadata import PROJECT_NAME
from .gui_tools import choose_file, zenity_available
from .lumberjack import debug, error, info, stop, warn
from .tools import cd, cwd, run_cmd
from .where import cwd_mover

PROGRAM_NAME = PACKAGE_NAME

pick_file = partial(choose_file,
                    initial_path=Path(f'src/{PROGRAM_NAME}/'),
                    filters=[('Python file', '*.py')]
                   ) # Chooses a Python file

@auto_doc(AUTO_DOC_HEAD)
def file_info(path: str, mime: bool = False, encoding: bool = False) -> str:
    """
    Return type information for a file, similar to the `file` command.

    :param path: Path to the file
    :param mime: If True, return MIME type (e.g., 'image/png')
    :param encoding: If True, return encoding info (e.g., 'utf-8')
    """
    if mime:
        ms = magic.Magic(mime=True)
    elif encoding:
        ms = magic.Magic(mime_encoding=True)
    else:
        ms = magic.Magic()

    return ms.from_file(str(Path(path)))
    
@auto_doc(AUTO_DOC_HEAD)
def is_hidden(p:str|Path) -> bool:
    return any(part.startswith('.') for part in Path(p).parts)

@auto_doc(AUTO_DOC_HEAD)
def is_visible(p:str|Path)->bool:
    return not is_hidden(p)

# --- Base File Factory ---
@auto_class_doc(AUTO_DOC_HEAD)
class File:
    _mime_registry: dict[str, type] = {}
    _ext_registry: dict[str, type] = {}
    _folder_registry: list[tuple[type, callable]] = []

    @auto_doc(AUTO_DOC_HEAD)
    def __new__(cls, p: str | Path | None = None):
        if cls is not File:
            return super().__new__(cls)
        if p is None:
            return super().__new__(cls)

        path = Path(p)

        # --- Folder detection ---
        if path.is_dir():
            for subclass, predicate in cls._folder_registry:
                try:
                    if predicate(path):
                        return super().__new__(subclass)
                except Exception:
                    continue
            return super().__new__(Folder)

        # --- Extension detection ---
        ext = path.suffix.lower()
        if ext in cls._ext_registry:
            return super().__new__(cls._ext_registry[ext])

        # --- MIME detection ---
        mime = cls._detect_mime(path)
        if mime:
            for pattern, subclass in cls._mime_registry.items():
                if mime.startswith(pattern):
                    return super().__new__(subclass)

        return super().__new__(cls)

    @auto_doc(AUTO_DOC_HEAD)
    def __init__(self, p: str | Path | None = None):
        self.path = Path(p) if p else None

    # --- MIME detection ---
    @staticmethod
    @auto_doc(AUTO_DOC_HEAD)
    def _detect_mime(path: Path) -> str | None:
        try:
            import magic  # optional
            return magic.from_file(str(path), mime=True)
        except Exception:
            mime, _ = mimetypes.guess_type(path)
            return mime

    # --- Registration decorators ---
    @classmethod
    @auto_doc(AUTO_DOC_HEAD)
    def register_mime(cls, pattern: str):
        def decorator(subclass):
            cls._mime_registry[pattern] = subclass
            return subclass
        return decorator

    @classmethod
    @auto_doc(AUTO_DOC_HEAD)
    def register_ext(cls, *exts: str):
        def decorator(subclass):
            for e in exts:
                cls._ext_registry[e.lower()] = subclass
            return subclass
        return decorator

    @classmethod
    @auto_doc(AUTO_DOC_HEAD)
    def register_folder(cls, predicate):
        def decorator(subclass):
            cls._folder_registry.append((subclass, predicate))
            return subclass
        return decorator

    # --- Delegation & Utilities ---
    @auto_doc(AUTO_DOC_HEAD)
    def __getattr__(self, name):
        if self.path and hasattr(self.path, name):
            return getattr(self.path, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    @auto_doc(AUTO_DOC_HEAD)
    def __truediv__(self, other):
        return File(self.path / other)

    @auto_doc(AUTO_DOC_HEAD)
    def __rtruediv__(self, other):
        return File(Path(other) / self.path)

    @auto_doc(AUTO_DOC_HEAD)
    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        return self.path == Path(other)

    @auto_doc(AUTO_DOC_HEAD)
    def __str__(self):
        return str(self.path) if self.path else "<no path>"

    @auto_doc(AUTO_DOC_HEAD)
    def __repr__(self):
        return f"{type(self).__name__}({self.path!r})"

    @auto_doc(AUTO_DOC_HEAD)
    def __fspath__(self):
        return str(self.path)

    @auto_doc(AUTO_DOC_HEAD)
    def output(self) -> str:
        if not self.path:
            return "[red]No path set[/red]"
        result = self.path.name
        if self.path.is_dir():
            result = f"[blue bold]{result}[/blue bold]"
        return result

    @auto_doc(AUTO_DOC_HEAD)
    def info(self):
        if not self.path:
            return None
        return file_info(str(self.path.resolve()))

    @auto_doc(AUTO_DOC_HEAD)
    def mime(self):
        if not self.path:
            return None
        return file_info(str(self.path.resolve()))

@auto_class_doc(AUTO_DOC_HEAD)
class Folder(File):
    def list(self):
        return [File(p) for p in self.path.iterdir()]

    def tree(self, depth: int = 2):
        def _walk(p, d):
            if d < 0: return
            for f in p.iterdir():
                print('  ' * (depth-d) + f.name)
                if f.is_dir():
                    _walk(f, d-1)
        _walk(self.path, depth)

@File.register_folder(lambda p: (p / "__init__.py").exists())
class PythonPackage(Folder):
    def info(self):
        return f"{self.path} (Python package)"

@File.register_folder(lambda p: (p / "Makefile").exists() or any(p.glob("*.c")))
class CProjectDir(Folder):
    def info(self):
        return f"{self.path} (C project directory)"

# Text / Source / Python / C Files

@File.register_mime("text/")
class TextFile(File):
    def read_lines(self) -> list[str]:
        return self.path.read_text(errors='ignore').splitlines() if self.path else []

    def write_lines(self, lines: list[str]):
        self.path.write_text('\n'.join(lines))

    def sed(self, inplace=False)-> bool:
        pass

@File.register_ext(".cfg")
class ConfigFile(TextFile):
    """Simple key=value config file handler."""
    
    def read(self) -> dict[str, str]:
        data = {}
        if not self.path or not self.path.exists(): 
            return data
        for line in self.path.read_text().splitlines():
            line = line.split('#', 1)[0].strip()  # strip comments
            if not line: 
                continue
            key, sep, value = line.partition('=')
            if sep:
                data[key.strip()] = value.strip()
        return data

    def write(self, data: dict[str, str]):
        lines = [f"{k} = {v}" for k, v in data.items()]
        self.path.write_text('\n'.join(lines))

class SrcFile(TextFile):
    """Generic source file."""
    pass

# Python files
@File.register_ext(".py")
class PyFile(SrcFile):
    def pick(self):
        """ Prompt the user to choose a Python `*.py` file. """
        self.path = choose_file(
            initial_path=cwd(),
            filters=[('Python file', '*.py')]
        )
        if self.path:
            info(f'User chose {self.path}')
        else:
            info("User cancelled.")

    def is_in_package(self) -> bool:
        return (self.path.parent / '__init__.py').exists()

    @cwd_mover()
    def run(self) -> subprocess.CompletedProcess | None:
        if not self.path: 
            self.pick()
        if not self.path:
            return None

        if self.is_in_package():
            debug(f'File {str(self.path)} is in a package folder.')
            cd(self.path.parent.parent)
            debug(f'Changed to directory {cwd()}')
            process = run_cmd([
                sys.executable,
                '-m',
                f'{self.path.parent.name}.{self.path.stem}'
            ])
        else:
            process = run_cmd([sys.executable, str(self.path)])

        cd(self.run._CWD)
        debug(f'Changed back to {cwd()}')
        return process

# C source files
@File.register_ext(".c", ".h")
class CFile(SrcFile):
    """Represents a C source or header file."""
    def compile(self, output: str | None = None) -> subprocess.CompletedProcess:
        """Compile the C file with gcc."""
        if output is None:
            output = self.path.stem
        return run_cmd(["gcc", str(self.path), "-o", str(output)])


class TempFile(File):
    def __enter__(self):
        self.path = Path(tempfile.mktemp())
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        try: self.path.unlink()
        except FileNotFoundError: pass

class TempFolder(Folder):
    def __enter__(self):
        self.path = Path(tempfile.mkdtemp())
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.path, ignore_errors=True)

class ExecutableFile(File):
    def run(self, args: list[str] = None) -> subprocess.CompletedProcess:
        if args is None: args = []
        return subprocess.run([str(self.path)] + args, capture_output=True, text=True)

if __name__ == '__main__':
    print(f"Running {Path(__file__).name}")
    from .where import DEBUG, TESTING
    print(f'{TESTING=}')
    print(f'{DEBUG=}')
    print(f'{debug=}')
    if TESTING:
        debug('Running a PyFile...')
        p = PyFile().run()
        if not p:
            print("User cancelled.")
            # exit()
        else:
            code_color = 'red' if p.returncode else 'green'
            output = StringIO()
            rp(f"""
    [cyan]Called process results[/cyan]:
    Return code: [{code_color}]{p.returncode}[/{code_color}]""", file=output)
            if p.stderr:
                rp(f"""
    {('Error output: \n' + p.stderr + '\n') if p.stderr else ''}""", file=output)
            if p.stdout:
                rp(f"""
    {('Standard output: \n' + p.stdout + '\n') if p.stdout else ''}""", file=output)
            print(output.getvalue().strip())
            print()
        examples = [
    "/etc/hosts",
    "setup.py",
    "main.c",
    "/usr/share/pixmaps/debian-logo.png",
    "/usr/lib/python3.12",
    "/usr/src/linux",
]
        
        for e in examples:
            f = File(e)
            print(f"{f.path!s:40} -> {type(f).__name__}")

