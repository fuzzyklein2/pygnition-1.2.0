# --- Calendar (best-effort) ------------------------------------------------
class CalendarDialog(Dialog):
    def __init__(self, title: str = "Select Date"):
        self.title = title

    def run(self) -> Optional[str]:
        # Try to import tkcalendar; if not present, ask for YYYY-MM-DD input
        try:
            from tkcalendar import Calendar
        except Exception:
            # fallback
            root = tk.Tk()
            root.withdraw()
            res = simpledialog.askstring(self.title, "Enter date (YYYY-MM-DD):", parent=root)
            root.destroy()
            return res
        root = tk.Tk()
        root.title(self.title)
        cal = Calendar(root, selectmode='day')
        cal.pack(padx=10, pady=10)
        sel = {}
        def on_ok():
            sel['date'] = cal.get_date()
            root.destroy()
        ttk.Button(root, text="OK", command=on_ok).pack(pady=6)
        root.mainloop()
        return sel.get('date')

# --- Lists, checklist, radiolist -------------------------------------------
class ListDialog(Dialog):
    def __init__(self, title: str = "Select", columns: Sequence[str] = ("Item",), data: Sequence[Sequence[str]] = (), multiple: bool = False):
        self.title = title
        self.columns = list(columns)
        self.data = list(data)
        self.multiple = multiple

    def run(self) -> Optional[List[Sequence[str]]]:
        root = tk.Tk()
        root.title(self.title)
        tree = ttk.Treeview(root, columns=self.columns, show='headings', selectmode='extended' if self.multiple else 'browse')
        for c in self.columns:
            tree.heading(c, text=c)
            tree.column(c, width=150, anchor='w')
        for row in self.data:
            tree.insert('', 'end', values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        res = []
        def on_ok():
            sel = tree.selection()
            for iid in sel:
                res.append(tree.item(iid, 'values'))
            root.destroy()
        btns = ttk.Frame(root)
        ttk.Button(btns, text="OK", command=on_ok).pack(side=tk.LEFT, padx=6, pady=6)
        ttk.Button(btns, text="Cancel", command=root.destroy).pack(side=tk.LEFT, padx=6, pady=6)
        btns.pack()
        root.mainloop()
        return res or None

class ChecklistDialog(Dialog):
    def __init__(self, title: str = "Checklist", items: Sequence[Tuple[str,str]] = ()):
        # items: sequence of (value, label)
        self.title = title
        self.items = list(items)

    def run(self) -> List[str]:
        root = tk.Tk()
        root.title(self.title)
        vars = {}
        for val, label in self.items:
            v = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(root, text=label, variable=v)
            chk.pack(anchor='w', padx=6, pady=2)
            vars[val] = v
        res = []
        def on_ok():
            for k, v in vars.items():
                if v.get():
                    res.append(k)
            root.destroy()
        ttk.Button(root, text="OK", command=on_ok).pack(pady=6)
        root.mainloop()
        return res

class RadiolistDialog(Dialog):
    def __init__(self, title: str = "Choose one", items: Sequence[Tuple[str,str]] = ()):
        # items: sequence of (value, label)
        self.title = title
        self.items = list(items)

    def run(self) -> Optional[str]:
        root = tk.Tk()
        root.title(self.title)
        var = tk.StringVar(value=None)
        for val, label in self.items:
            rb = ttk.Radiobutton(root, text=label, variable=var, value=val)
            rb.pack(anchor='w', padx=6, pady=2)
        sel = {}
        def on_ok():
            sel['v'] = var.get()
            root.destroy()
        ttk.Button(root, text="OK", command=on_ok).pack(pady=6)
        root.mainloop()
        return sel.get('v')

# --- Scale / Color / Progress / About ------------------------------------
class ScaleDialog(Dialog):
    def __init__(self, title: str = "Scale", label: str = "", minval: int = 0, maxval: int = 100, initial: int = 50):
        self.title = title
        self.label = label
        self.min = minval
        self.max = maxval
        self.initial = initial

    def run(self) -> int:
        root = tk.Tk()
        root.title(self.title)
        ttk.Label(root, text=self.label).pack(padx=6, pady=6)
        scale = ttk.Scale(root, from_=self.min, to=self.max, orient=tk.HORIZONTAL)
        scale.set(self.initial)
        scale.pack(fill=tk.X, padx=10, pady=6)
        sel = {}
        def on_ok():
            sel['v'] = int(scale.get())
            root.destroy()
        ttk.Button(root, text="OK", command=on_ok).pack(pady=6)
        root.mainloop()
        return sel.get('v')

class ColorSelectionDialog(Dialog):
    def __init__(self, title: str = "Choose Color"):
        self.title = title

    def run(self) -> Optional[Tuple[Tuple[int,int,int], str]]:
        root = tk.Tk()
        root.withdraw()
        res = colorchooser.askcolor(title=self.title, parent=root)
        root.destroy()
        # returns ((r,g,b), hex) or (None,None)
        return res

