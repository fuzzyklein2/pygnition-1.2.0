# dialogs/progress_and_about.py
from .dialog import Dialog
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Optional

class ProgressDialog(Dialog):
    def __init__(self, maximum: int = 100, auto_close: bool = True, indeterminate: bool = False, title: str = "Progress"):
        super().__init__(title)
        self.maximum = maximum
        self.auto_close = auto_close
        self.indeterminate = indeterminate
        self._root_window = None
        self._progress = None

    def start(self):
        if self._root_window:
            return
        self._root_window = tk.Toplevel(self.parent)
        self._root_window.title(self.title)
        self._progress = ttk.Progressbar(self._root_window, maximum=self.maximum,
                                         mode='indeterminate' if self.indeterminate else 'determinate', length=300)
        self._progress.pack(padx=10, pady=10)
        if self.indeterminate:
            self._progress.start()
        t = threading.Thread(target=self._root_window.mainloop, daemon=True)
        t.start()

    def update(self, value: int):
        if not self._progress or self.indeterminate:
            return
        self._progress['value'] = value
        if value >= self.maximum and self.auto_close:
            self.stop()

    def stop(self):
        if not self._root_window:
            return
        try:
            self._root_window.quit()
            self._root_window.destroy()
        finally:
            self._root_window = None
            self._progress = None

    def run(self):
        self._root_window = tk.Toplevel(self.parent)
        self._root_window.title(self.title)
        progress = ttk.Progressbar(self._root_window, maximum=self.maximum, mode='determinate', length=300)
        progress.pack(padx=10, pady=10)
        ttk.Button(self._root_window, text="Close", command=self._root_window.destroy).pack(pady=6)
        self._root_window.mainloop()

