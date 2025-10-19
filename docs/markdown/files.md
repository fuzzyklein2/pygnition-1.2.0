# Module `files`

<a name='module-files'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [magic](https://pypi.org/project/magic/)
- [os](https://docs.python.org/3/library/os.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)

## Module Data

<a name='files-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`

## Function **choose_file**

<a name='files-function-choose_file'></a>
```python
choose_file(title='Select a file', directory=False, multiple=False, save=False, confirm_overwrite=True, initial_path=None, filters=None, check_existence=True, relative_path=False, create_dirs=True, always_list=False, single_path=False)
```

Open a Zenity file chooser dialog and return selected file path(s).

Falls back to [command](driver.md#driver-class-driver-method-command)-line input if Zenity is not available
or if no display environment is present.

Parameters
----------
title : str
    Window title for the dialog.
directory : bool
    If True, choose a directory instead of a file.
multiple : bool
    If True, allow multiple selections.
save : bool
    If True, show a 'Save As' dialog instead of 'Open [File](files.md#files-class-file)'.
confirm_overwrite : bool
    If True, ask for confirmation before overwriting (used with save=True).
initial_path : str | Path | None
    Optional starting path (directory or file name).
filters : list[tuple[str, str]] | None
    A list of (name, pattern) pairs.
check_existence : bool
    If True, verify existence (open mode) or [warn](lumberjack.md#lumberjack-function-warn)/auto-create (save mode).
relative_path : bool
    If True, returned paths are relative to current working directory.
create_dirs : bool
    If True and save=True, auto-create parent directories if missing.
always_list : bool
    If True, always return a list of Path objects, even for single selection.
single_path : bool
    If True, always return a single Path (first item if multiple selected).
    Overrides `always_list`.

Returns
-------
Path | list[Path] | None
    A Path object, or list of Paths, or None if user cancels.

## Function **file_info**

<a name='files-function-file_info'></a>
```python
file_info(path, mime=False, encoding=False)
```

Return type information for a file, similar to the `file` [command](driver.md#driver-class-driver-method-command).

:param path: Path to the file
:param [mime](files.md#files-class-file-method-mime): If True, return MIME type (e.g., 'image/png')
:param encoding: If True, return encoding [info](lumberjack.md#lumberjack-function-info) (e.g., 'utf-8')

## Class **File**

<a name='files-class-file'></a>
```python
File()
```

### Method **output**

<a name='files-class-file-method-output'></a>
```python
output(self)
```

### Method **info**

<a name='files-class-file-method-info'></a>
```python
info(self)
```

### Method **mime**

<a name='files-class-file-method-mime'></a>
```python
mime(self)
```

