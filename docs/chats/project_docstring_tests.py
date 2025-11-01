"""
Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: PROJECT_NAME
Version: 1.0.0
Author: Test Author
Date: LAST_SAVED_DATE

## Description

This module defines the Project class, representing a Python project folder
with helpers for type detection, version parsing, requirements, author,
description, and GitHub URL deduction.

## Typical Use

```python
args = parse_arguments()
```

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

## GitHub

## ──────────────────────────────
## Doctest Examples with Temporary Project Folders, Git, GUI, Script, CGI
## ──────────────────────────────

>>> import tempfile, shutil
>>> from pathlib import Path
>>> from pygnition.files.projects import Project, looks_like_project

# -------------------------------
# Basic project setup with .git and Filter class
# -------------------------------
>>> temp_dir = tempfile.mkdtemp()
>>> temp_path = Path(temp_dir) / "myproject-1.2.3"
>>> temp_path.mkdir()
>>> src = temp_path / "src" / "myproject"
>>> src.mkdir(parents=True)
>>> (src / "__main__.py").write_text("print('Hello')")
>>> (src / "myproject.py").write_text("class FilterExample: pass")
>>> data_dir = src / "data"
>>> data_dir.mkdir()
>>> (data_dir / "author.txt").write_text("Test Author")
>>> (data_dir / "description.txt").write_text("Test description")
>>> (temp_path / "requirements.txt").write_text("requests\nnumpy")
>>> (temp_path / ".git").mkdir()

>>> p = Project(temp_path)
>>> p.name
'myproject'
>>> p.version
'1.2.3'
>>> p.deduce_github()
'https://github.com/<your-username>/myproject-1.2.3.git'
>>> p.get_author()
'Test Author'
>>> p.get_description()
'Test description'
>>> sorted(p.read_requirements().split())
['numpy', 'requests']
>>> p.detect_type() == p.Types.FILTER
True
>>> ctx = p.detect_context()
>>> ctx['is_git_repo'] == True
True
>>> looks_like_project(temp_path)
True
>>> isinstance(p.describe(), str)
True

# -------------------------------
# TK GUI detection
# -------------------------------
>>> tk_path = Path(temp_dir) / "tk_project-0.1"
>>> tk_path.mkdir(parents=True)
>>> tk_src = tk_path / "src" / "tk_project"
>>> tk_src.mkdir(parents=True)
>>> (tk_src / "__main__.py").write_text("import tkinter\nprint('Tk project')")

>>> tk_p = Project(tk_path)
>>> tk_p.detect_type() == tk_p.Types.TK
True

# -------------------------------
# GTK GUI detection
# -------------------------------
>>> gtk_path = Path(temp_dir) / "gtk_project-0.1"
>>> gtk_path.mkdir(parents=True)
>>> gtk_src = gtk_path / "src" / "gtk_project"
>>> gtk_src.mkdir(parents=True)
>>> (gtk_src / "__main__.py").write_text("from gi.repository import Gtk\nprint('GTK project')")

>>> gtk_p = Project(gtk_path)
>>> gtk_p.detect_type() == gtk_p.Types.GTK
True

# -------------------------------
# Single-file script detection
# -------------------------------
>>> script_path = Path(temp_dir) / "single_script-0.1"
>>> script_path.mkdir()
>>> (script_path / "solo.py").write_text("print('Just one file')")

>>> script_p = Project(script_path)
>>> script_p.detect_type() == script_p.Types.SCRIPT
True

# -------------------------------
# CGI / web front-end detection
# -------------------------------
>>> cgi_path = Path(temp_dir) / "cgi_project-0.1"
>>> cgi_path.mkdir()
>>> cgi_src = cgi_path / "src" / "cgi_project"
>>> cgi_src.mkdir(parents=True)
>>> (cgi_src / "index.html").write_text("<html></html>")

>>> cgi_p = Project(cgi_path)
>>> cgi_p.detect_type() == cgi_p.Types.CGI
True

# Cleanup all temporary folders
>>> shutil.rmtree(temp_dir)
"""
