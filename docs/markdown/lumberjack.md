# Module `lumberjack`

<a name='module-lumberjack'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [datetime](https://docs.python.org/3/library/datetime.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [sys](https://docs.python.org/3/library/sys.html)

## Module Data

<a name='lumberjack-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`
<a name='lumberjack-var-log_picts'></a>
- **LOG_PICTS** = `{logging.DEBUG: DEBUG_PICT, logging.INFO: INFO_PICT, logging.WARNING: WARNING_PICT, logging.ERROR: ERROR_PICT, logging.CRITICAL: CRITICAL_PICT}`

## Function **setuplog**

<a name='lumberjack-function-setuplog'></a>
```python
setuplog(LOGFILE, level)
```

## Function **log**

<a name='lumberjack-function-log'></a>
```python
log(level, message)
```

## Function **debug**

<a name='lumberjack-function-debug'></a>
```python
debug(message)
```

## Function **info**

<a name='lumberjack-function-info'></a>
```python
info(message)
```

## Function **warn**

<a name='lumberjack-function-warn'></a>
```python
warn(message)
```

## Function **error**

<a name='lumberjack-function-error'></a>
```python
error(message)
```

## Function **stop**

<a name='lumberjack-function-stop'></a>
```python
stop(message)
```

