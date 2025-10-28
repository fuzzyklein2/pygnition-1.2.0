## CI-Ready Python Project Template

This Markdown contains the full instructions and setup for a Python project template that is CI-ready and automatically generates version numbers.

---

## 1. Project structure

```
myproject/
├── .github/
│   └── workflows/
│       └── ci.yml
├── mypackage/
│   ├── __init__.py
│   └── _version.py       # generated automatically
├── pyproject.toml
├── setup.py
└── write_version.py
```

---

## 2. `write_version.py` (CI-ready)

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path
from datetime import datetime
import os

VERSION_FILE = Path("mypackage/_version.py")
DEFAULT_VERSION = "0.0.0"

def get_git_version():
    """Return Git tag-based version, or None if Git is unavailable."""
    try:
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--dirty"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        version = None
    return version

def append_ci_build(version):
    """Append CI or nightly build identifier."""
    ci_build = os.getenv("CI_BUILD")  # e.g., GitHub Actions run number
    if ci_build:
        return f"{version}+ci.{ci_build}"
    else:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"{version}+dev.{timestamp}"
    
def write_version_file(filename=VERSION_FILE):
    version = get_git_version()
    if version is None:
        if filename.exists():
            version = filename.read_text().strip().split('=')[-1].strip().strip('"')
        else:
            version = DEFAULT_VERSION

    version = append_ci_build(version)

    content = f'__version__ = "{version}"\n'

    if filename.exists() and filename.read_text() == content:
        print(f"{filename} is up-to-date ({version})")
        return

    filename.write_text(content)
    print(f"Wrote {filename} with version: {version}")

if __name__ == "__main__":
    write_version_file()
```

---

## 3. `setup.py` (with build hooks)

```python
#!/usr/bin/env python3
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist

class build_py(_build_py):
    def run(self):
        subprocess.run(["python", "write_version.py"], check=True)
        super().run()

class sdist(_sdist):
    def run(self):
        subprocess.run(["python", "write_version.py"], check=True)
        super().run()

setup(
    name="mypackage",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    cmdclass={
        "build_py": build_py,
        "sdist": sdist,
    },
)
```

---

## 4. `mypackage/__init__.py`

```python
from ._version import __version__
__all__ = ["__version__"]
```

---

## 5. `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"
```

---

## 6. GitHub Actions workflow (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      CI_BUILD: ${{ github.run_number }}

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install build tools
      run: python -m pip install --upgrade pip build wheel

    - name: Generate version
      run: python write_version.py

    - name: Build package
      run: python -m build

    - name: Test package (optional)
      run: |
        python -m pip install dist/*.whl
        python -c "import mypackage; print(mypackage.__version__)"
```

---

### Features

1. Automatic versioning using Git tags or commit hashes.
2. Appends CI build number or dev timestamp for nightly builds.
3. Automatically generates `_version.py` included in wheel and sdist.
4. Compatible with `pip install`, wheels, sdist, and GitHub Actions.
5. Professional workflow similar to projects like `numpy` and `requests`.

