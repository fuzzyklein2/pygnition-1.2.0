#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️ WARNING! ⚠️ ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PKG_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {str(last_saved_datetime(__file__).date()).split('.')[0]}

## Description

This module defines the Workshop class.

## Typical Use
```python
app = Workshop()
app.run()

Notes
-----
You can include implementation notes, dependencies, or version-specific
details here.

"""



import atexit
import http.server
from pathlib import Path
import socketserver
import sys
import threading
import webbrowser

# DEBUG = not __debug__

# This block is temporary until `pygnition. is actually installed.
# I don't want to make re-installing it a constant part of testing it yet.
'''
LOCATION_PATH = Path.home() / '.pygnition.location.txt'
IGNITION_PATH = LOCATION_PATH.read_text().strip()
sys.path.insert(0, str(IGNITION_PATH))
'''

from pygnition.picts import *
from pygnition.settings import *

class MyTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.server_name = "localhost"
        self.server_port = server_address[1]
        self.allow_reuse_address = True

class Server(Settings):
    def __init__(self, project_dir=PROJECT_DIR):
        super().__init__()
        atexit.register(self.shutdown)

        # config_file = USER_PREFS_DIR / 'server.cfg'
        # if not config_file.exists():
        #     config_file = PROJECT_DIR / 'etc/config.ini'
        # if not config_file.exists():
        #     config_file = PYGNITION_DIRECTORY / 'etc/config.ini'
        # assert(config_file.exists())
        # super().__init__(config=configure(config_file))
        # if not hasattr(self, 'host'):
        #     warn('Server configuration file does not exist!')
        #     debug(f'{self.config=}')
        #     debug('Setting default host.')
        #     self.host = '127.0.0.1'
        # if not hasattr(self, 'port'):
        #     debug('Setting default port.')
        #     self.port = 8888

        self.project_dir = project_dir
        self.cgi_dir = self.project_dir / 'cgi-bin'
        if not self.cgi_dir.exists():
            stop(f'CGI folder is missing! {WORRIED_PICT}')

        self.user_data_dir = USER_DATA_DIR

        self.httpd = None
        self.thread = None

        self.port = int(self.port)

        debug(f'''Initialized {PROGRAM_NAME}:

Server object dir: {pformat([s for s in dir(self) if not s.startswith('_')])}''')
        debug(f'''Configuration:

Configuration files: {str(CONFIG_FILES)}
Host: {self.host}
Port: {self.port}
`hwww` data directory: {USER_DATA_DIR}
Project directory: {PROJECT_DIR}
Program path: {PROGRAM_PATH}
Log file: {self.logfile}
ConfigParser: {self.config}
''')


    def run(self):
        debug(f'Running {PROGRAM_NAME}')
        self.start()

    def shutdown(self):
        print(f"{CHECK_PICT}Execution complete.")
        print(f'{WAVE_PICT}Goodbye!')

    def start(self):
        """Start HTTP server in a background thread."""
        if self.thread and self.thread.is_alive():
            info("Server already running.")
            return

        try:
            self.thread = threading.Thread(target=self._serve, daemon=True)
            self.thread.start()
        except OSError as e:
            print(e)

        info(f'Server thread started on {self.host}:{self.port}')

    def _serve(self):
        os.chdir(self.project_dir)
        handler = http.server.CGIHTTPRequestHandler
        handler.cgi_directories = ['/cgi-bin']

        with MyTCPServer((self.host, self.port), handler) as self.httpd:
            # info(f'Serving project at {self.project_dir} on {self.host}:{self.port}')

            # index_file = self.project_dir / 'index.html'
            # if index_file.exists():
            #     webbrowser.open(f'http://{self.host}:{self.port}/index.html')

            try:
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                info('Server stopped.')
            except OSError:
                stop('Address already in use!')

    def stop(self):
        """Shut down the server if it's running."""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            info('Server stopped.')

if __name__ == '__main__':
    Server().run()
