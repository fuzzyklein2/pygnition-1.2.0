# Module `where`

<a name='module-where'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [enum](https://docs.python.org/3/library/enum.html)
- [inspect](https://docs.python.org/3/library/inspect.html)
- [os](https://docs.python.org/3/library/os.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pygnition](https://docs.python.org/3/library/pygnition.html)
- [sys](https://docs.python.org/3/library/sys.html)

## Module Data

<a name='where-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`
<a name='where-var-running_cli'></a>
- **RUNNING_CLI** = `False`
<a name='where-var-running_console'></a>
- **RUNNING_CONSOLE** = `False`
<a name='where-var-running_in_jupyter'></a>
- **RUNNING_IN_JUPYTER** = `False`
<a name='where-var-running_gateway'></a>
- **RUNNING_GATEWAY** = `False`
<a name='where-var-debug'></a>
- **DEBUG** = `False`
<a name='where-var-verbose'></a>
- **VERBOSE** = `False`
<a name='where-var-warnings'></a>
- **WARNINGS** = `False`
<a name='where-var-testing'></a>
- **TESTING** = `False`
<a name='where-var-program_name'></a>
- **PROGRAM_NAME** = `'UNKNOWN'`
<a name='where-var-program_path'></a>
- **PROGRAM_PATH** = `None`
<a name='where-var-calling_module'></a>
- **CALLING_MODULE** = `None`
<a name='where-var-callers'></a>
- **CALLERS** = `import_chain()`
<a name='where-var-program_name'></a>
- **PROGRAM_NAME** = `PROJECT_DIR.stem.split('-')[0]`
<a name='where-var-project_name'></a>
- **PROJECT_NAME** = `PROGRAM_NAME`
<a name='where-var-pygnition_directory'></a>
- **PYGNITION_DIRECTORY** = `Path(getsourcefile(Interpreters)).parent.parent`
<a name='where-var-user_data_dir'></a>
- **USER_DATA_DIR** = `Path.home() / f'.{PROJECT_NAME}'`
<a name='where-var-user_prefs_dir'></a>
- **USER_PREFS_DIR** = `USER_DATA_DIR / 'etc'`
<a name='where-var-debug'></a>
- **DEBUG** = `bool({'-d', '--debug'}.intersection(sys.argv))`
<a name='where-var-verbose'></a>
- **VERBOSE** = `bool({'-v', '--verbose'}.intersection(sys.argv))`
<a name='where-var-warnings'></a>
- **WARNINGS** = `bool({'-w', '--warnings'}.intersection(sys.argv))`
<a name='where-var-testing'></a>
- **TESTING** = `bool({'-t', '--test'}.intersection(sys.argv))`

## Function **display_where_info**

<a name='where-function-display_where_info'></a>
```python
display_where_info()
```

Test this module from any project directory that imports it.

