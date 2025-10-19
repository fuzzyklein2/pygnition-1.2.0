#!/usr/bin/env python3
"""
generate_docs_pipeline.py

Generates Markdown documentation for all modules in a Python project.

Features:
    • Works from any directory (script can live anywhere)
    • Safely imports modules even with relative imports
    • Skips hidden files/folders, __pycache__, and internal boilerplate modules
    • Optionally recursive
    • Saves Markdown to docs/markdown/
    • Includes a table of contents
"""

import os
import sys
import runpy
import traceback
from pathlib import Path
from importlib import import_module
from datetime import datetime

# Default excluded directories
DEFAULT_EXCLUDED_DIRS = {"__pycache__", ".git", ".ipynb_checkpoints"}

# --- Utilities -------------------------------------------------------------

def prepare_project_dir(project_dir: str | Path | None = None) -> Path:
    """Resolve project_dir, add it (and its parent) to sys.path, and chdir there."""
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir).resolve()

    # Add project_dir and its parent to sys.path
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))
    parent = project_dir.parent
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))

    # Change to the project directory to make relative imports happy
    os.chdir(project_dir)

    return project_dir


def safe_import_module(module_name: str, project_dir: Path):
    """Import module safely, handling relative imports and collecting tracebacks."""
    try:
        module_globals = runpy.run_module(module_name, run_name="__main__", alter_sys=True)
        return module_globals, None
    except Exception:
        return None, traceback.format_exc()


def generate_module_doc(py_file: Path, project_dir: Path, markdown_dir: Path):
    """Generate a Markdown doc for a single .py file."""
    rel_path = py_file.relative_to(project_dir)
    module_name = ".".join(rel_path.with_suffix("").parts)
    md_file = markdown_dir / rel_path.with_suffix(".md")
    md_file.parent.mkdir(parents=True, exist_ok=True)

    module_globals, tb = safe_import_module(module_name, project_dir)

    with md_file.open("w", encoding="utf-8") as f:
        f.write(f"# Module `{module_name}`\n\n")
        f.write(f"*Generated on {datetime.now().isoformat(timespec='seconds')}*\n\n")

        if tb:
            f.write(f"❌ **Failed to import module `{module_name}`**\n\n```\n{tb}\n```\n")
            return module_name, md_file

        doc = module_globals.get("__doc__", "").strip() or "(No docstring found.)"
        f.write(doc + "\n")

    return module_name, md_file


def generate_toc(markdown_dir: Path):
    """Generate a Table of Contents for all generated Markdown files."""
    toc_file = markdown_dir / "_TOC.md"
    with toc_file.open("w", encoding="utf-8") as f:
        f.write("# Documentation Index\n\n")
        for md_file in sorted(markdown_dir.rglob("*.md")):
            if md_file.name == "_TOC.md":
                continue
            rel = md_file.relative_to(markdown_dir)
            name = rel.with_suffix("").as_posix()
            f.write(f"- [{name}](./{rel.as_posix()})\n")


# --- Main pipeline --------------------------------------------------------

def generate_docs(project_dir: str | Path | None = None, recursive: bool = True, excluded_dirs=None):
    project_dir = prepare_project_dir(project_dir)
    markdown_dir = Path(project_dir) / "docs" / "markdown"
    markdown_dir.mkdir(parents=True, exist_ok=True)

    excluded_dirs = set(excluded_dirs or [])
    excluded_dirs |= DEFAULT_EXCLUDED_DIRS

    skipped_files = {"__init__.py", "startmeup.py", "initools.py"}

    py_files = []
    for root, dirs, files in os.walk(project_dir):
        if not recursive and Path(root) != project_dir:
            continue

        # Skip hidden and excluded directories
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".") and d not in excluded_dirs
        ]

        for f in files:
            if (
                f.endswith(".py")
                and not f.startswith(".")
                and f not in skipped_files
            ):
                py_files.append(Path(root) / f)

    print(f"📚 Found {len(py_files)} Python files in {project_dir}")

    for py_file in py_files:
        module_name, md_file = generate_module_doc(py_file, project_dir, markdown_dir)
        print(f"  📝 {module_name} → {md_file.relative_to(project_dir)}")

    generate_toc(markdown_dir)
    print("\n✅ Documentation generation complete.\n")


# --- CLI entrypoint -------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for a Python project."
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Path to the project directory (default: current directory)."
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not recurse into subdirectories."
    )
    args = parser.parse_args()

    generate_docs(args.project_dir, recursive=not args.no_recursive)
