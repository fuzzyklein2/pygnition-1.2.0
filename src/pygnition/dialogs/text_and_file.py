# dialogs/text_and_file.py
from .dialog import Dialog
from .constants import DEFAULT_PADDING
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog, colorchooser
from typing import Optional, Sequence, Tuple, Dict, List

# --- Text / Notification dialogs ---
class TextInfoDialog(Dialog):
    def __init__(self, text: str, title: str = "Text", width: int = 60, height: int = 20):
        super().__init__(title, width, height)
        self.text = text

    def run(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        txt = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=self.width, height=self.height)
        txt.insert("1.0", self.text)
        txt.configure(state="disabled")
        txt.pack(fill=tk.BOTH, expand=True)
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=DEFAULT_PADDING)
        self.window.mainloop()

class NotificationDialog(Dialog):
    def __init__(self, text: str, title: str = "Notification", timeout: Optional[float] = 3.0):
        super().__init__(title)
        self.text = text
        self.timeout = timeout

    def run(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry('+100+100')
        lbl = ttk.Label(self.window, text=self.text)
        lbl.pack(padx=10, pady=10)
        if self.timeout:
            self.window.after(int(self.timeout*1000), self.window.destroy)
        self.window.mainloop()

# --- File / directory selection dialogs ---
class FileSelectionDialog(Dialog):
    def __init__(self, title: str = "Select File", multiple: bool = False, save: bool = False,
                 filetypes=None, initialdir: str = ""):
        super().__init__(title)
        self.multiple = multiple
        self.save = save
        self.filetypes = filetypes or [("All files", "*")]
        self.initialdir = initialdir

    def run(self) -> Optional[Sequence[str]]:
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        if self.save:
            res = filedialog.asksaveasfilename(title=self.title, filetypes=self.filetypes,
                                               initialdir=self.initialdir, parent=self.window)
            self.window.destroy()
            return res or None
        if self.multiple:
            res = filedialog.askopenfilenames(title=self.title, filetypes=self.filetypes,
                                              initialdir=self.initialdir, parent=self.window)
            self.window.destroy()
            return list(res)
        else:
            res = filedialog.askopenfilename(title=self.title, filetypes=self.filetypes,
                                             initialdir=self.initialdir, parent=self.window)
            self.window.destroy()
            return res or None

class DirectorySelectionDialog(Dialog):
    def __init__(self, title: str = "Select Directory", initialdir: str = ""):
        super().__init__(title)
        self.initialdir = initialdir

    def run(self) -> Optional[str]:
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        res = filedialog.askdirectory(title=self.title, initialdir=self.initialdir, parent=self.window)
        self.window.destroy()
        return res or None

# --- Entry / Password / Form dialogs ---
class EntryDialog(Dialog):
    def __init__(self, prompt: str = "", title: str = "Input"):
        super().__init__(title)
        self.prompt = prompt

    def run(self) -> Optional[str]:
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        res = simpledialog.askstring(self.title, self.prompt, parent=self.window)
        self.window.destroy()
        return res

class PasswordDialog(Dialog):
    def __init__(self, prompt: str = "", title: str = "Password"):
        super().__init__(title)
        self.prompt = prompt

    def run(self) -> Optional[str]:
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        res = simpledialog.askstring(self.title, self.prompt, show="*", parent=self.window)
        self.window.destroy()
        return res

class FormsDialog(Dialog):
    def __init__(self, fields: Sequence[Tuple[str,str]] = (), title: str = "Form"):
        super().__init__(title)
        self.fields = list(fields)

    def run(self) -> Optional[Dict[str,str]]:
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        entries = {}
        for name, label in self.fields:
            frm = ttk.Frame(self.window)
            ttk.Label(frm, text=label).pack(side=tk.LEFT, padx=6, pady=6)
            ent = ttk.Entry(frm)
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[name] = ent
            frm.pack(fill=tk.X, padx=6)

        result = {}
        def on_ok():
            for k, e in entries.items():
                result[k] = e.get()
            self.window.destroy()

        def on_cancel():
            nonlocal result
            result = None
            self.window.destroy()

        btns = ttk.Frame(self.window)
        ttk.Button(btns, text="OK", command=on_ok).pack(side=tk.LEFT, padx=6, pady=6)
        ttk.Button(btns, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=6, pady=6)
        btns.pack()
        self.window.mainloop()
        return result
