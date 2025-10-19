# Module `settings`

<a name='module-settings'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [logging](https://docs.python.org/3/library/logging.html)
- [os](https://docs.python.org/3/library/os.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pprint](https://docs.python.org/3/library/pprint.html)
- [pygnition](https://docs.python.org/3/library/pygnition.html)
- [shutil](https://docs.python.org/3/library/shutil.html)
- [types](https://docs.python.org/3/library/types.html)

## Module Data

<a name='settings-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`
<a name='settings-var-input'></a>
- **INPUT** = `get_piped_input()`
<a name='settings-var-args_file'></a>
- **ARGS_FILE** = `PROJ_DATA / 'std_opts.csv'`
<a name='settings-var-config_files'></a>
- **CONFIG_FILES** = `[USER_PREFS_DIR / s for s in os.listdir(USER_PREFS_DIR) if Path(s).suffix in {'.ini', '.cfg'}]`
<a name='settings-var-log_file'></a>
- **LOG_FILE** = `USER_DATA_DIR / f'logs/{PROGRAM_NAME}.log'`
<a name='settings-var-args'></a>
- **ARGS** = `None`
<a name='settings-var-env'></a>
- **ENV** = `Environment()`
<a name='settings-var-config'></a>
- **CONFIG** = `None`
<a name='settings-var-log_level'></a>
- **LOG_LEVEL** = `logging.WARNING`
<a name='settings-var-settings'></a>
- **SETTINGS** = `dict()`

## Class **Settings**

<a name='settings-class-settings'></a>
```python
Settings()
```

### Method **dumps**

<a name='settings-class-settings-method-dumps'></a>
```python
dumps(self)
```

### Method **dump**

<a name='settings-class-settings-method-dump'></a>
```python
dump(self)
```

