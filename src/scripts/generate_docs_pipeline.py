#!/usr/bin/env python3
"""
generate_docs_pipeline.py

Generates Markdown documentation for a Python project in src/<PROJECT_NAME>/.

Assumes:
  • Current working directory is project root
  • .venv is active (optional)
  • Project installed in editable mode for import-link resolution (optional)

Outputs:
  • Module Markdown files in docs/markdown/
  • Table of contents in docs/_TOC.md
  • Optional dependency graph in docs/markdown/dependencies.svg

Features:
  • AST-based (no project code execution)
  • Top-level variables/constants with inline comment extraction
  • Full docstrings included with automatic cross-links to internal symbols
  • Imports section linking to stdlib docs, known external docs, or internal modules
  • Optional hiding of private modules/files and private members (--include-private)
  • Optional non-recursive mode (--no-recursive)
"""

import ast
from pathlib import Path
from datetime import datetime
import re
import importlib.util

# Optional Graphviz for dependency graph
try:
    from graphviz import Digraph
except Exception:
    Digraph = None

# --- Config ---------------------------------------------------------------
EXCLUDED_DIRS = {".ipynb_checkpoints", "__pycache__", ".git"}
DEFAULT_SKIPPED_FILES = {"__init__.py", "startmeup.py", "initools.py"}
IMPORT_RE = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', re.MULTILINE)
EXTERNAL_DOCS = {
    "numpy": "https://numpy.org/doc/stable/",
    "pandas": "https://pandas.pydata.org/docs/",
    "requests": "https://docs.python-requests.org/",
    "matplotlib": "https://matplotlib.org/stable/contents.html",
    "scipy": "https://docs.scipy.org/doc/scipy/",
}

# --- Utilities ------------------------------------------------------------
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-")

def format_signature(node: ast.AST) -> str:
    """Return a signature string for function or class AST node, with default values."""
    if isinstance(node, ast.FunctionDef):
        args = []
        total_args = len(node.args.args)
        defaults = [None] * (total_args - len(node.args.defaults)) + node.args.defaults
        for arg, default in zip(node.args.args, defaults):
            if default is not None:
                try:
                    default_val = ast.unparse(default) if hasattr(ast, "unparse") else "..."
                except Exception:
                    default_val = "..."
                args.append(f"{arg.arg}={default_val}")
            else:
                args.append(arg.arg)
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")
        return f"({', '.join(args)})"
    elif isinstance(node, ast.ClassDef):
        return "()"
    return "(...)"

def find_imports(text: str):
    return {m.group(1).split('.')[0] for m in IMPORT_RE.finditer(text)}

def extract_top_level_vars(py_file: Path):
    """
    Return list of tuples (name, value_repr, comment) for top-level constants/variables.
    Trailing inline comment on the same line is captured as comment.
    """
    vars_info = []
    text = py_file.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except Exception:
        return vars_info
    lines = text.splitlines()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    try:
                        value = ast.unparse(node.value) if hasattr(ast, "unparse") else "..."
                    except Exception:
                        value = "..."
                    comment = None
                    line_no = node.lineno - 1
                    if 0 <= line_no < len(lines):
                        line = lines[line_no]
                        if "#" in line:
                            comment_text = line.split("#", 1)[1].strip()
                            comment = comment_text
                    vars_info.append((name, value, comment))
    return vars_info

def get_source_files(src_dir: Path, include_private: bool, skipped_files=None):
    """
    Return a list of python source files under src_dir, honoring excluded dirs
    and optionally skipping private module files (those starting with '_').
    """
    skipped_files = set(skipped_files or DEFAULT_SKIPPED_FILES)
    py_files = []
    for f in src_dir.rglob("*.py"):
        # Skip in excluded directories
        if any(part in EXCLUDED_DIRS for part in f.parts):
            continue
        # Skip configured filenames
        if f.name in skipped_files:
            continue
        # Skip ipynb checkpoints double-safe
        if ".ipynb_checkpoints" in f.parts:
            continue
        # Skip private module files unless include_private True
        if not include_private and f.name.startswith("_"):
            continue
        py_files.append(f)
    return sorted(py_files)

def link_docstring(doc: str, cross_ref_map: dict) -> str:
    """Replace occurrences of cross-ref names in docstring with Markdown links."""
    if not doc:
        return ""
    keys_sorted = sorted(cross_ref_map.keys(), key=len, reverse=True)
    if not keys_sorted:
        return doc
    pattern = r'\b(' + '|'.join(re.escape(k) for k in keys_sorted) + r')\b'
    def replacer(match):
        name = match.group(0)
        link = cross_ref_map.get(name)
        return f"[{name}]({link})" if link else name
    return re.sub(pattern, replacer, doc)

# --- Main generator -------------------------------------------------------
def generate_docs(project_name: str, recursive: bool = True, include_private: bool = False, skipped_files=None):
    """
    Generate Markdown documentation for package under src/<project_name>.
    - recursive: whether to recurse into subpackages
    - include_private: whether to include private modules/files and private members
    - skipped_files: optional set of filenames to skip
    """
    src_dir = Path("src") / project_name
    if not src_dir.exists():
        raise FileNotFoundError(f"Package directory {src_dir} does not exist.")

    markdown_dir = Path("docs") / "markdown"
    markdown_dir.mkdir(parents=True, exist_ok=True)

    skipped_files = set(skipped_files or DEFAULT_SKIPPED_FILES)

    # Collect source files (respect include_private)
    py_files = get_source_files(src_dir, include_private=include_private, skipped_files=skipped_files)
    if not recursive:
        py_files = [f for f in py_files if f.parent == src_dir]

    print(f"📚 Found {len(py_files)} Python files in {src_dir}")

    # Module map: filename stem -> markdown file name (flat)
    module_map = {f.stem: f"{f.stem}.md" for f in py_files}

    # Build cross-reference map: classes/functions/methods/vars -> anchor
    cross_ref_map = {}
    for py_file in py_files:
        module_name = ".".join(py_file.relative_to(src_dir).with_suffix("").parts)
        text = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except Exception:
            tree = ast.Module(body=[])
        # functions & classes
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                name = node.name
                if not include_private and name.startswith("_"):
                    continue
                anchor_type = "class" if isinstance(node, ast.ClassDef) else "function"
                cross_ref_map[name] = f"{module_map[py_file.stem]}#{slugify(f'{module_name}-{anchor_type}-{name}')}"
            # methods
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef):
                        if not include_private and sub.name.startswith("_"):
                            continue
                        cross_ref_map[sub.name] = f"{module_map[py_file.stem]}#{slugify(f'{module_name}-class-{node.name}-method-{sub.name}')}"
        # top-level vars
        for name, _, _ in extract_top_level_vars(py_file):
            if not include_private and name.startswith("_"):
                continue
            cross_ref_map[name] = f"{module_map[py_file.stem]}#{slugify(f'{module_name}-var-{name}')}"

    # Helper: produce correct import link
    def import_link(name: str) -> str:
        # internal package module
        if name in module_map:
            return module_map[name]
        # try to detect stdlib vs site-packages
        try:
            spec = importlib.util.find_spec(name)
        except Exception:
            spec = None
        if spec and getattr(spec, "origin", None):
            origin = spec.origin or ""
            # Heuristic: if origin doesn't include site-packages or dist-packages then it's stdlib
            if "site-packages" not in origin and "dist-packages" not in origin:
                return f"https://docs.python.org/3/library/{name}.html"
        return EXTERNAL_DOCS.get(name) or f"https://pypi.org/project/{name}/"

    # Delete old markdown files (flat)
    for old_md in (markdown_dir).glob("*.md"):
        try:
            old_md.unlink()
        except Exception:
            pass

    toc_entries = []

    # Generate markdown files
    for py_file in py_files:
        module_name = ".".join(py_file.relative_to(src_dir).with_suffix("").parts)
        md_file = markdown_dir / f"{py_file.stem}.md"
        text = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except Exception:
            tree = ast.Module(body=[])

        with md_file.open("w", encoding="utf-8") as f:
            f.write(f"# Module `{module_name}`\n\n")
            anchor = slugify(f"module-{module_name}")
            toc_entries.append((1, module_name, f"{md_file.name}#{anchor}"))
            f.write(f"<a name='{anchor}'></a>\n")
            f.write(f"*Generated on {datetime.now().isoformat(timespec='seconds')}*\n\n")

            # Imports section (internal / stdlib / external)
            imports = find_imports(text)
            if imports:
                f.write("## Imports\n\n")
                for imp in sorted(imports):
                    # optionally hide private import names? imports are package names, not members.
                    link = import_link(imp)
                    f.write(f"- [{imp}]({link})\n")
                f.write("\n")

            # Top-level variables/constants
            vars_info = extract_top_level_vars(py_file)
            vars_info = [t for t in vars_info if (include_private or not t[0].startswith("_"))]
            if vars_info:
                f.write("## Module Data\n\n")
                for name, value, comment in vars_info:
                    var_anchor = slugify(f"{module_name}-var-{name}")
                    f.write(f"<a name='{var_anchor}'></a>\n")
                    f.write(f"- **{name}** = `{value}`")
                    if comment:
                        f.write(f" — {comment}")
                    f.write("\n")
                f.write("\n")

            # Classes & functions
            for node in tree.body:
                # Classes
                if isinstance(node, ast.ClassDef):
                    if not include_private and node.name.startswith("_"):
                        continue
                    f.write(f"## Class **{node.name}**\n\n")
                    class_anchor = slugify(f"{module_name}-class-{node.name}")
                    toc_entries.append((2, node.name, f"{md_file.name}#{class_anchor}"))
                    f.write(f"<a name='{class_anchor}'></a>\n")
                    doc = ast.get_docstring(node)
                    if doc:
                        f.write(link_docstring(doc.strip(), cross_ref_map) + "\n\n")
                    f.write(f"```python\n{node.name}{format_signature(node)}\n```\n\n")

                    # Methods
                    for sub in node.body:
                        if isinstance(sub, ast.FunctionDef):
                            if not include_private and sub.name.startswith("_"):
                                continue
                            f.write(f"### Method **{sub.name}**\n\n")
                            method_anchor = slugify(f"{module_name}-class-{node.name}-method-{sub.name}")
                            toc_entries.append((3, sub.name, f"{md_file.name}#{method_anchor}"))
                            f.write(f"<a name='{method_anchor}'></a>\n")
                            f.write(f"```python\n{sub.name}{format_signature(sub)}\n```\n\n")
                            doc = ast.get_docstring(sub)
                            if doc:
                                f.write(link_docstring(doc.strip(), cross_ref_map) + "\n\n")

                # Top-level functions
                elif isinstance(node, ast.FunctionDef):
                    if not include_private and node.name.startswith("_"):
                        continue
                    f.write(f"## Function **{node.name}**\n\n")
                    func_anchor = slugify(f"{module_name}-function-{node.name}")
                    toc_entries.append((2, node.name, f"{md_file.name}#{func_anchor}"))
                    f.write(f"<a name='{func_anchor}'></a>\n")
                    f.write(f"```python\n{node.name}{format_signature(node)}\n```\n\n")
                    doc = ast.get_docstring(node)
                    if doc:
                        f.write(link_docstring(doc.strip(), cross_ref_map) + "\n\n")

    # Write _TOC.md (flat list with anchors)
    toc_file = markdown_dir.parent / "_TOC.md"
    with toc_file.open("w", encoding="utf-8") as f:
        f.write("# Documentation Index\n\n")
        for level, name, link in toc_entries:
            indent = "  " * (level - 1)
            f.write(f"{indent}- [{name}]({link})\n")

    # Optional dependency graph (internal modules only)
    if Digraph:
        g = Digraph('Dependencies', format='svg')
        g.attr(rankdir='LR')
        for mod_name in module_map:
            # hide private modules if requested
            if not include_private and mod_name.startswith("_"):
                continue
            g.node(mod_name)
        for py_file in py_files:
            mod_name = ".".join(py_file.relative_to(src_dir).with_suffix("").parts)
            if not include_private and mod_name.split(".")[-1].startswith("_"):
                continue
            text = py_file.read_text(encoding="utf-8")
            for imp in find_imports(text):
                if imp in module_map:
                    if not include_private and imp.startswith("_"):
                        continue
                    g.edge(mod_name, imp)
        graph_file = markdown_dir / "dependencies"
        g.render(str(graph_file), cleanup=True)
        print(f"🖼 Dependency graph generated at {graph_file}.svg")

    print("\n✅ Documentation generation complete.\n")

# --- CLI entrypoint -------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Markdown docs for src/<PROJECT_NAME>")
    parser.add_argument("project_name", help="Name of the Python package in src/")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recurse into subdirectories")
    parser.add_argument("--include-private", action="store_true", help="Include private modules/files and members (names starting with '_')")
    parser.add_argument("--skip-files", nargs="*", help="Filenames to skip (space-separated). e.g. --skip-files foo.py bar.py")
    args = parser.parse_args()

    skipped = set(args.skip_files) if args.skip_files else None
    generate_docs(args.project_name, recursive=not args.no_recursive, include_private=args.include_private, skipped_files=skipped)
