# 🔥`pygnition`🔥 

#### Python package meant to simplify the scripting process.

## Version
### 1.0.1c
This project is brand new, although it's based on code I've been playing around with for years. I wouldn't trust it for anything serious until it's been more completely tested. That said, I'm not having any serious problems with it or anything. 🤷

## ⚠️ WARNING! ⚠️

#### This project is _UNDER CONSTRUCTION_!




<p align="center">
  <img src="/home/fuzzy/projects/pygnition-1.2.0c/image/Under_Construction01_transparent.gif" alt="Cute little anime girl with an "Under Construction" sign." width="400">
</p>



## Requirements

## Development

## Usage

`pygnition` can be used to write a few different types of Python scripts without duplicating the boilerplate code required to:

* Gather configuration settings from files
* Gather environment variables relevant to the script
* Parse the command line arguments and options

In addition, as part of this process, `pygnition` will automatically determine its location, the current working directory, and a hidden data directory associated with the project's name. (For this reason, a project using pygnition should _not_ be named something suicidal like `bashrc`, for instance.)

## Examples

### Hello, 🌎!

Scripts using `pygnition` are designed to be run as modules. Navigate to the project directory `$IGNITION_DIR/docs/examples/hw-1.0.1` and enter:

```bash
py -m hw

The output should be:

```bash
Hello, 🌎!

#### 📝 Note:

`pygnition` depends pretty heavily on Unicode support. If your system or terminal doesn't have that, this is probably not the software you are looking for. 

The `-t` (or `--testing`) option provides more output:

```bash
$ py -m hw -t
⚙️  Logging configuration complete.
🗃️  Log file: <$HOME>.hw/logs/hw.log
🕔  Current time: 2025-10-11 16:52:45.173176
🐞  Running hw
⚠️  hw is under construction!

🐞  HW settings:

Application directory: <$HOME>/projects/pygnition-1.0.1/docs/examples/hw-1.0.1
Data directory:        <$HOME>/.hw

Command line options:
{'all': False,
 'config': None,
 'debug': False,
 'follow': False,
 'input': None,
 'log': None,
 'output': None,
 'quiet': False,
 'recursive': False,
 'testing': True,
 'verbose': False,
 'warnings': False}

Command line arguments:
[]

    Defined in <$HOME>/projects/pygnition-1.0.1/docs/examples/hw-1.0.1/data/std_opts.csv

Environment variables:
{}

Configuration files:
[PosixPath('<$HOME>/.hw/etc/server.cfg')]

Configuration:
{'host': '127.0.0.1', 'logfile': 'logs/program.log', 'port': '8888'}

Hello, 🌎!

#### Source Code

##### `hw.py`

```python
from pygnition.picts import *
from pygnition.program import Program
from pygnition.lumberjack import info, warn

class HW(Program):
    def __init__(self):
        super().__init__()

    def test(self):
        warn(f'{self.name} is under construction!')
        self.dump()

    def run(self):
        super().run()
        print(f'Hello, {GLOBE_AMERICA_PICT.strip()} !')


##### `__main__.py`

```python
from .hw import *

if __name__ == '__main__':
    HW().run()


#### 📋 TODO:
