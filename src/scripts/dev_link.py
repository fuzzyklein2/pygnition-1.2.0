#!/usr/bin/env python3
"""
Link a Python package into the active virtual environment's site-packages for development.

- Only creates symlinks for folders that exist inside the package.
- Supports package folder itself and optional resource folders:
  data/, etc/, html/, image/, scripts/
- Usage:
    source .venv/bin/activate
    python dev_link.py /full/path/to/package
"""

import sys
from pathlib import Path
import site

# Resource folders to optionally link if present in the package
OPTIONAL_FOLDERS = ["data", "etc", "html", "image", "scripts"]

def link_package(package_path: Path):
    package_path = package_path.resolve()
    if not package_path.is_dir():
        print(f"Error: {package_path} is not a directory.")
        sys.exit(1)

    # Detect active venv's site-packages
    venv_site_packages = next((Path(p) for p in site.getsitepackages() if 'site-packages' in p), None)
    if not venv_site_packages:
        print("Error: Could not find site-packages in the active environment.")
        sys.exit(1)

    # Link the main package folder
    package_symlink = venv_site_packages / package_path.name
    if package_symlink.exists():
        if package_symlink.is_symlink():
            package_symlink.unlink()
        else:
            print(f"Error: {package_symlink} exists and is not a symlink.")
            sys.exit(1)
    package_symlink.symlink_to(package_path, target_is_directory=True)
    print(f"Linked package: {package_path.name} → {package_symlink}")

    # Symlink optional folders only if they exist
    for folder in OPTIONAL_FOLDERS:
        folder_path = package_path / folder
        if folder_path.exists() and folder_path.is_dir():
            target_symlink = venv_site_packages / folder
            if target_symlink.exists():
                if target_symlink.is_symlink():
                    target_symlink.unlink()
                else:
                    print(f"Warning: {target_symlink} exists and is not a symlink. Skipping.")
                    continue
            target_symlink.symlink_to(folder_path, target_is_directory=True)
            print(f"Linked folder: {folder_path.name} → {target_symlink}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python dev_link.py /full/path/to/package")
        sys.exit(1)

    package_path = Path(sys.argv[1])
    link_package(package_path)

if __name__ == "__main__":
    main()
