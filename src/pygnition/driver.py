#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PACKAGE_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {LAST_SAVED_DATE}

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

## [GitHub]({get_upstream_url()})


"""

import argparse
from argparse import ArgumentParser as AP
from cmd import Cmd
import logging
from pathlib import Path
from pprint import pp
import shlex
import shutil
from types import SimpleNamespace

from rich import print as rp

from pygnition.arguments import get_args
from pygnition.configure import configure
# from pygnition.constants import EPILOG
from pygnition.environment import Environment
from pygnition.lumberjack import debug, error, info, stop, warn
from pygnition.program import Program
from pygnition.settings import Settings, SETTINGS
from pygnition.tools import chk_cmd, run_cmd
from pygnition.where import PROJ_DATA, USER_PREFS_DIR


class Driver(Cmd, Program):

    class Command(SimpleNamespace):
        @auto_doc("Initialize the `Command` object.")
        def __init__(self, name, *args, **kwargs):
            # self.driver = driver
            super().__init__(**kwargs)
            # self.driver = kwargs['driver']
            # self.dump()
            self.cmd_name = name
            self.log = logging.getLogger(name)
            LEVEL = logging.WARN
            if self.debug or self.testing:
                LEVEL = logging.DEBUG
                self.verbose = True
            elif self.verbose: LEVEL = logging.INFO
            self.log.setLevel(LEVEL)
            self.log.info('Command object initialized.')
            # self.log.critical(f'{self.app_dir}')

        def run(self):
            debug(f'Running the {self.cmd_name} command ...')
            # TODO: Does the log level need to be reset? My guess is probably not but logging is weird.

        def dump(self):
            pp(vars(self))
            
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self)
        Program.__init__(self, *args, **kwargs)
        self.current_cmd = None

    def preloop(self):
        """Called once when the cmdloop() method is called, before entering the command loop."""
        print(f"Welcome to {self.program_name}!")
        print("Type 'help' for a list of commands.")
        print()
        self.prompt = f"[{self.program_name}]: "

    def do_done(self, line):
        self.poker_table.reset()
        print()
        self.prompt = f"Ready for {'the' if self.poker_table.status else 'a'} {PROMPTS[self.poker_table.status]}: "

    # def revise(self):
        # self.poker_table.revise()
        

    @auto_doc("Parse the command line as if it were actually a command line.")
    def get_opts(self, name:str, line:str)->argparse.Namespace|None:
        line = shlex.split(line)
        OPTS_FILE = self.app_dir / 'data' / f'{name}_opts.csv'
        print(f'{OPTS_FILE=}')
        if not OPTS_FILE.exists():
            warn(f'File {str(OPTS_FILE)} is missing.')
            OPTS_FILE = self.app_dir / 'data' / 'std_opts.csv'
        options = list()
        if OPTS_FILE.exists():
            options = get_args(OPTS_FILE)
        ap = AP(prog=name,
                description='',
                epilog=(PROJ_DATA / 'epilog.txt').read_text().strip())

        for opt in options:
            ap.add_argument(*opt[0], **opt[1])

        return ap.parse_args(line)

    def command(self, name:str, line:str):
        debug(f'''Doing command.
{name=}
{line=}
{self.__class__.__name__=}
''')
        settings = dict()
        config = None
        config_file = USER_PREFS_DIR / f'etc/{name}.cfg'
        if config_file.exists():
            config = configure([config_file])
            if config:
                settings.update(dict(config.config['DEFAULT']))
        settings.update(Environment(self.program_name.upper() + '_' + name.upper() + '_'))
        options = self.get_opts(name, line)
        if options: settings.update(vars(options))
        # self.log = logging.getLogger(self.name)

        # pp(settings)
        
        getattr(self, f'{name.title()}')(name, driver=self, **settings).run()

    @property
    def current_cmd(self):
        return self._current_cmd

    @current_cmd.setter
    def current_cmd(self, s:str | None):
        self._current_cmd = s

    @current_cmd.deleter
    def current_cmd(self):
        del self._current_cmd

    def run(self):
        super().cmdloop()

    def do_quit(self, args):
        """Exit the application."""
        return True

    # def preloop(self):
    #     debug('Running driver ...')

    @classmethod
    def find_class(cls, name):
        '''Return the member class whose name matches `name` (case-insensitive).'''
        for attr_name, attr_value in vars(cls).items():
            if isinstance(attr_value, type) and attr_name.lower() == name.lower():
                return attr_value
        return None

    def default(self, line):
        """See if the first word of `line` matches a `Command` class object in `dir(self)`."""
        lines = shlex.split(line)
        command = lines[0]
        _class = self.find_class(command)
        if _class:
            self.command(command, ' '.join(lines[1:]))
        elif command.startswith('!'):
            # Attempt to run `line` with subprocess.
            chk_cmd(' '.join([lines[0][1:] if len(lines[0]) > 1 else '', *lines[1:]]))
        else:
            # Attempt to interpret the line as Python
            try:
                eval(line)
            except:
                warn('Invalid command')

if __name__ == '__main__':
    d = Driver()
    d.run()
