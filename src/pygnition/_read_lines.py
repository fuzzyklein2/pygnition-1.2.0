from functools import singledispatch
from pathlib import Path

ERROR = f"❗  ERROR: "

@singledispatch
def read_lines(arg)->None:
    print(f"{ERROR}read_lines : Bad argument")

@read_lines.register
def _(p:Path)->list|None:
    try:
        return p.read_text().splitlines()
    except FileNotFoundError:
        print(f'{ERROR} File {str(p)} does not exist!')

@read_lines.register
def _(s:str)->list|None:
    return read_lines(Path(s))
