# Module `driver`

<a name='module-driver'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [argparse](https://docs.python.org/3/library/argparse.html)
- [cmd](https://docs.python.org/3/library/cmd.html)
- [logging](https://docs.python.org/3/library/logging.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pygnition](https://docs.python.org/3/library/pygnition.html)
- [shlex](https://docs.python.org/3/library/shlex.html)
- [shutil](https://docs.python.org/3/library/shutil.html)

## Module Data

<a name='driver-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`

## Class **Driver**

<a name='driver-class-driver'></a>
```python
Driver()
```

### Method **get_opts**

<a name='driver-class-driver-method-get_opts'></a>
```python
get_opts(self, name, line)
```

### Method **command**

<a name='driver-class-driver-method-command'></a>
```python
command(self, name, line)
```

### Method **current_cmd**

<a name='driver-class-driver-method-current_cmd'></a>
```python
current_cmd(self)
```

### Method **current_cmd**

<a name='driver-class-driver-method-current_cmd'></a>
```python
current_cmd(self, s)
```

### Method **current_cmd**

<a name='driver-class-driver-method-current_cmd'></a>
```python
current_cmd(self)
```

### Method **run**

<a name='driver-class-driver-method-run'></a>
```python
run(self)
```

### Method **do_quit**

<a name='driver-class-driver-method-do_quit'></a>
```python
do_quit(self, args)
```

Exit the application.

### Method **preloop**

<a name='driver-class-driver-method-preloop'></a>
```python
preloop(self)
```

### Method **find_class**

<a name='driver-class-driver-method-find_class'></a>
```python
find_class(cls, name)
```

Return the member class whose name matches `name` (case-insensitive).

### Method **default**

<a name='driver-class-driver-method-default'></a>
```python
default(self, line)
```

See if the first word of `line` matches a `Command` class object in `dir(self)`.

