# Module `generate_docs_pipeline`

<a name='module-generate_docs_pipeline'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [argparse](https://docs.python.org/3/library/argparse.html)
- [ast](https://docs.python.org/3/library/ast.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [graphviz](https://pypi.org/project/graphviz/)
- [importlib](https://docs.python.org/3/library/importlib.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [re](https://docs.python.org/3/library/re.html)

## Module Data

<a name='generate_docs_pipeline-var-excluded_dirs'></a>
- **EXCLUDED_DIRS** = `{'.ipynb_checkpoints', '__pycache__', '.git'}`
<a name='generate_docs_pipeline-var-default_skipped_files'></a>
- **DEFAULT_SKIPPED_FILES** = `{'__init__.py', 'startmeup.py', 'initools.py'}`
<a name='generate_docs_pipeline-var-import_re'></a>
- **IMPORT_RE** = `re.compile('^\\s*(?:import|from)\\s+([a-zA-Z_][a-zA-Z0-9_\\.]*)', re.MULTILINE)`
<a name='generate_docs_pipeline-var-external_docs'></a>
- **EXTERNAL_DOCS** = `{'numpy': 'https://numpy.org/doc/stable/', 'pandas': 'https://pandas.pydata.org/docs/', 'requests': 'https://docs.python-requests.org/', 'matplotlib': 'https://matplotlib.org/stable/contents.html', 'scipy': 'https://docs.scipy.org/doc/scipy/'}`

## Function **slugify**

<a name='generate_docs_pipeline-function-slugify'></a>
```python
slugify(text)
```

## Function **format_signature**

<a name='generate_docs_pipeline-function-format_signature'></a>
```python
format_signature(node)
```

Return a signature string for function or class AST node, with [default](driver.md#driver-class-driver-method-default) values.

## Function **find_imports**

<a name='generate_docs_pipeline-function-find_imports'></a>
```python
find_imports(text)
```

## Function **extract_top_level_vars**

<a name='generate_docs_pipeline-function-extract_top_level_vars'></a>
```python
extract_top_level_vars(py_file)
```

Return list of tuples (name, value_repr, comment) for top-level constants/variables.
Trailing inline comment on the same line is captured as comment.

## Function **get_source_files**

<a name='generate_docs_pipeline-function-get_source_files'></a>
```python
get_source_files(src_dir, include_private, skipped_files=None)
```

Return a list of python source files under src_dir, honoring excluded dirs
and optionally skipping private module files (those starting with '_').

## Function **link_docstring**

<a name='generate_docs_pipeline-function-link_docstring'></a>
```python
link_docstring(doc, cross_ref_map)
```

Replace occurrences of cross-ref names in docstring with Markdown links.

## Function **generate_docs**

<a name='generate_docs_pipeline-function-generate_docs'></a>
```python
generate_docs(project_name, recursive=True, include_private=False, skipped_files=None)
```

Generate Markdown documentation for package under src/<project_name>.
- recursive: whether to recurse into subpackages
- include_private: whether to include private modules/files and private members
- skipped_files: optional set of filenames to skip

