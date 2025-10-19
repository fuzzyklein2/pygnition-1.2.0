# Module `tools`

<a name='module-tools'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [functools](https://docs.python.org/3/library/functools.html)
- [logging](https://docs.python.org/3/library/logging.html)
- [os](https://docs.python.org/3/library/os.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [rich](https://pypi.org/project/rich/)
- [subprocess](https://docs.python.org/3/library/subprocess.html)

## Module Data

<a name='tools-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`
<a name='tools-var-run_cmd'></a>
- **run_cmd** = `partial(run, encoding='utf-8', capture_output=True, check=True)`

## Function **cwd**

<a name='tools-function-cwd'></a>
```python
cwd()
```

## Function **pwd**

<a name='tools-function-pwd'></a>
```python
pwd()
```

## Function **cd**

<a name='tools-function-cd'></a>
```python
cd(p)
```

## Function **public**

<a name='tools-function-public'></a>
```python
public(obj)
```

## Function **yes_or_no**

<a name='tools-function-yes_or_no'></a>
```python
yes_or_no(question, message=None)
```

## Function **chk_cmd**

<a name='tools-function-chk_cmd'></a>
```python
chk_cmd(arg)
```

## Function **mkdir**

<a name='tools-function-mkdir'></a>
```python
mkdir(arg)
```

## Function **touch**

<a name='tools-function-touch'></a>
```python
touch(arg)
```

## Function **get_func_name**

<a name='tools-function-get_func_name'></a>
```python
get_func_name(func)
```

Sets `name = ` the function's name.

## Function **get_func_name2**

<a name='tools-function-get_func_name2'></a>
```python
get_func_name2(func)
```

Nearly identical to `[get_func_name](tools.md#tools-function-get_func_name)` but does not assume a [Driver](driver.md#driver-class-driver) class
called it.

## Function **subdirs**

<a name='tools-function-subdirs'></a>
```python
subdirs(arg=None, all=False)
```

Return a list of top-level subdirectories of `arg`
(or the current directory if `arg` is None).

Hidden directories are included only if `all=True`.

