# Module `server`

<a name='module-server'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [atexit](https://docs.python.org/3/library/atexit.html)
- [http](https://docs.python.org/3/library/http.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pygnition](https://docs.python.org/3/library/pygnition.html)
- [socketserver](https://docs.python.org/3/library/socketserver.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [webbrowser](https://docs.python.org/3/library/webbrowser.html)

## Module Data

<a name='server-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`

## Class **MyTCPServer**

<a name='server-class-mytcpserver'></a>
```python
MyTCPServer()
```

## Class **Server**

<a name='server-class-server'></a>
```python
Server()
```

### Method **run**

<a name='server-class-server-method-run'></a>
```python
run(self)
```

### Method **shutdown**

<a name='server-class-server-method-shutdown'></a>
```python
shutdown(self)
```

### Method **start**

<a name='server-class-server-method-start'></a>
```python
start(self)
```

Start HTTP server in a background thread.

### Method **stop**

<a name='server-class-server-method-stop'></a>
```python
stop(self)
```

Shut down the server if it's running.

