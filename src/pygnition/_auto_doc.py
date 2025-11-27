#!/usr/bin/env python3

from pathlib import Path

from ._metadata import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Package: 🔥  pygnition 🔥
Module: {MODULE_NAME}
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

import inspect, re, textwrap

from datetime import date
from pathlib import Path

unwrap = __import__('inspect').unwrap

AUTO_DOC_HEAD = '## `{name}`\n{version} : {date}'

def auto_doc(heading_template=None, heading_level=2):
    """
    Decorator that preserves the original function docstring and
    appends auto-generated Markdown tables for parameters and return types.
    Optionally adds a heading template at the top.

    This version:
    - Extracts inline comments for parameters and return values.
    - Falls back to reading the source file directly if inspect.getsource() fails.
    - Works safely with other decorators (e.g., @singledispatch, @staticmethod).
    """

    def extract_param_and_return_comments(func):
        """Extract inline comments for parameters and return type."""
        src = None
        try:
            src = inspect.getsource(func)
        except (OSError, TypeError):
            # fallback: read from file directly
            try:
                src = Path(func.__code__.co_filename).read_text()
                # find just the function definition portion
                pattern = (
                    r"def\s+%s\s*\((.*?)\)\s*(->[^#:]*)?(:|\n)" % func.__name__
                )
                m = re.search(pattern, src, re.S)
                if m:
                    src = "def " + func.__name__ + "(" + m.group(1) + ")"
            except Exception:
                src = ""

        src = textwrap.dedent(src)
        # Strip decorators
        src = re.sub(r"(?m)^@\w+.*\n", "", src)
        # Extract everything from 'def name(' to first colon
        m = re.search(r"def\s+\w+\s*\((.*?)\)\s*(->[^#:]*)?(:|\n)", src, re.S)
        if not m:
            return {}, None
        params_block = m.group(1)

        # Extract return-line part for return comment
        ret_match = re.search(r"\)\s*->[^#]*#\s*(.+)", src)
        return_comment = ret_match.group(1).strip() if ret_match else None

        param_comments = {}
        # Split by commas but preserve line breaks for multi-line signatures
        for chunk in re.split(r",\s*(?=[\w_*]+)", params_block):
            chunk = chunk.strip()
            if not chunk:
                continue
            # Match "name[: type][= default][# comment]"
            m2 = re.match(r"(\*{0,2}\w+)(?:\s*:[^=#]*)?(?:\s*=[^#]*)?(?:\s*#\s*(.*))?", chunk)
            if m2:
                name, comment = m2.groups()
                if comment:
                    param_comments[name] = comment.strip()

        return param_comments, return_comment

    def decorator(func):
        # Unwrap to reach the original underlying function if wrapped by another decorator
        real_func = inspect.unwrap(func)

        sig = inspect.signature(real_func)
        orig_doc = real_func.__doc__ or ""
        lines = []

        # Optional heading
        # if heading_template:
        sig = inspect.signature(real_func)
        hashes = "#" * heading_level
        lines.append(f"{hashes} {real_func.__name__}")
        lines.append(f"{VERSION} : {LAST_SAVED_DATE}")
        lines.append(f"##### {real_func.__name__}{str(sig)}")
        lines.append("")

        # Preserve existing docstring
        if orig_doc.strip():
            lines.append(orig_doc.strip())
            lines.append("")

        # Extract inline comments
        param_comments, return_comment = extract_param_and_return_comments(real_func)

        # Parameters
        if sig.parameters:
            lines.append("#### Parameters\n")
            lines.append("Name | Type(s) | Description")
            lines.append("--- | --- | ---")

            for name, param in sig.parameters.items():
                annot = param.annotation
                if annot == inspect.Parameter.empty:
                    annot_str = "Any"
                elif isinstance(annot, type):
                    annot_str = annot.__name__
                else:
                    annot_str = str(annot)

                default = (
                    f" *(default={param.default})*"
                    if param.default != inspect.Parameter.empty
                    else ""
                )

                desc = param_comments.get(name, "")
                lines.append(f"`{name}` | {annot_str}{default} | {desc}")

            lines.append("")

        # Returns
        return_annot = sig.return_annotation
        if return_annot == inspect.Signature.empty:
            return_annot_str = "Any"
        elif isinstance(return_annot, type):
            return_annot_str = return_annot.__name__
        else:
            return_annot_str = str(return_annot)

        lines.append("#### Returns\n")
        lines.append("Type | Description")
        lines.append("--- | ---")
        lines.append(f"`{return_annot_str}` | {return_comment or ''}")

        # Update the docstring on the real underlying function
        real_func.__doc__ = "\n".join(lines)

        return func  # Return the outer function (so existing decorators still see it)

    return decorator

def auto_class_doc(heading_template=None):
    """
    Decorator that auto-generates a Markdown-formatted docstring for a class.

    Features:
    - Adds an optional heading template with version/date.
    - Preserves and includes the original class docstring.
    - Parses `__init__` signature for parameters and inline `# comments`.
    - Lists public methods with signatures and first-line summaries.
    - Lists class attributes (constants, defaults, etc.).
    """

    def extract_param_comments(func):
        """Extract inline comments for parameters in a function definition."""
        src = None
        try:
            src = inspect.getsource(func)
        except (OSError, TypeError):
            try:
                src = Path(func.__code__.co_filename).read_text()
                pattern = r"def\s+%s\s*\((.*?)\)\s*(->[^#:]*)?(:|\n)" % func.__name__
                m = re.search(pattern, src, re.S)
                if m:
                    src = "def " + func.__name__ + "(" + m.group(1) + ")"
            except Exception:
                return {}

        src = textwrap.dedent(src)
        src = re.sub(r"(?m)^@\w+.*\n", "", src)  # strip decorators
        m = re.search(r"def\s+\w+\s*\((.*?)\)\s*(->[^#:]*)?(:|\n)", src, re.S)
        if not m:
            return {}

        params_block = m.group(1)
        param_comments = {}
        for chunk in re.split(r",\s*(?=[\w_*]+)", params_block):
            chunk = chunk.strip()
            if not chunk:
                continue
            m2 = re.match(
                r"(\*{0,2}\w+)(?:\s*:[^=#]*)?(?:\s*=[^#]*)?(?:\s*#\s*(.*))?", chunk
            )
            if m2:
                name, comment = m2.groups()
                if comment:
                    param_comments[name] = comment.strip()
        return param_comments

    def decorator(cls):
        orig_doc = inspect.getdoc(cls) or ""
        lines = []

        # Optional heading
        # if heading_template:
        init = getattr(cls, "__init__", None)
        sig = str(inspect.signature(init)) if init else "()"
        lines.append('<!-- -->')
        lines.append(f"## {cls.__name__}")
        lines.append(f"{VERSION} : {LAST_SAVED_DATE}")
        lines.append(f"##### {sig}")
        lines.append("")

        # Preserve class-level docstring
        if orig_doc:
            lines.append(orig_doc)
            lines.append("")

        # --- Constructor Parameters ---
        init = getattr(cls, "__init__", None)
        if init and hasattr(init, "__code__"):
            sig = inspect.signature(init)
            param_comments = extract_param_comments(init)
            params = [
                p for p in sig.parameters.values()
                if p.name != "self"
            ]
            if params:
                lines.append("#### Constructor Parameters\n")
                lines.append("Name | Type(s) | Description")
                lines.append("--- | --- | ---")

                for param in params:
                    annot = param.annotation
                    if annot == inspect.Parameter.empty:
                        annot_str = "Any"
                    elif isinstance(annot, type):
                        annot_str = annot.__name__
                    else:
                        annot_str = str(annot)

                    default = (
                        f" *(default={param.default})*"
                        if param.default != inspect.Parameter.empty
                        else ""
                    )

                    desc = param_comments.get(param.name, "")
                    lines.append(f"`{param.name}` | {annot_str}{default} | {desc}")

                lines.append("")

        # --- Class Attributes ---
        attrs = [
            (name, val)
            for name, val in vars(cls).items()
            if not name.startswith("_") and not inspect.isroutine(val)
        ]
        if attrs:
            lines.append("#### Attributes\n")
            lines.append("Name | Value | Type")
            lines.append("--- | --- | ---")
            for name, val in attrs:
                typename = type(val).__name__
                try:
                    val_repr = repr(val)
                    if len(val_repr) > 40:
                        val_repr = val_repr[:37] + "..."
                except Exception:
                    val_repr = "<unrepr>"
                lines.append(f"`{name}` | `{val_repr}` | `{typename}`")
            lines.append("")

        # --- Public Methods ---
        methods = [
            (name, m)
            for name, m in inspect.getmembers(cls, inspect.isfunction)
            if not name.startswith("_")
        ]
        if methods:
            lines.append("#### Methods\n")
            lines.append("Name | Signature | Description")
            lines.append("--- | --- | ---")

            for name, m in methods:
                sig = inspect.signature(m)
                doc = inspect.getdoc(m)
                desc = (doc.split("\n")[0] if doc else "")
                lines.append(f"`{name}` | `{sig}` | {desc}")

        cls.__doc__ = "\n".join(lines)
        return cls

    return decorator

# Example usage
@auto_doc()
def add( a: int,    # 1st number
         b: int = 0 # 2nd number
       ) -> int:    # sum of the numbers
    """Add two numbers together in a friendly way."""
    return a + b


@auto_doc()
def greet(name: str # name to greet
         ) -> str:  # full greeting
    """Say hello to someone."""
    return f"Hello, {name}!"

@auto_class_doc()
class Workshop:
    """Manage and build workshop projects."""

    DEFAULT_TIMEOUT = 30
    LOG_FILE = "workshop.log"

    @auto_doc(heading_level=3)
    def __init__(self, root:                  # Application folder
                 Path, verbose: bool = False, # whether to talk a lot
                 dry_run: bool = False        # simulate actions
                ):
        """Initialize a workshop environment."""
        self.root = root
        self.verbose = verbose
        self.dry_run = dry_run

    
    @auto_doc(heading_level=3)
    def build(self, force: bool = False):
        """Build the workshop project."""
        pass

    @auto_doc(heading_level=3)
    def clean(self):
        """Remove build artifacts."""
        pass

if __name__ == "__main__":
    print(add.__doc__)
    print("\n" + "-" * 40 + "\n")
    print(greet.__doc__)
    print("\n" + "-" * 40 + "\n")
    print(Workshop.__doc__)
    import doctest
    doctest.testmod()