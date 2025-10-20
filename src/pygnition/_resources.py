# src/quotes/resources.py
from importlib import resources
from pathlib import Path

# from .where import PROJECT_NAME

def load_data(folder: str, filename: str, text: bool = True) -> str | bytes:
    """
    Load a file from the package's `data` folder.

    Args:
        filename: Name of the file inside `quotes/data`.
        text: If True, return string. If False, return bytes.

    Returns:
        File contents as str (default) or bytes.

    Raises:
        FileNotFoundError if the file does not exist.
    """
    file_path = resources.files(f"{__package__}").joinpath(folder).joinpath(filename)
    if text:
        return file_path.read_text(encoding="utf-8")
    else:
        return file_path.read_bytes()


def data_path(filename: str) -> Path:
    """
    Return a pathlib.Path to a file in `quotes/data`.
    Useful if some API requires a Path object.

    Args:
        filename: Name of the file inside `quotes/data`.

    Returns:
        pathlib.Path
    """
    return resources.files(f"{__package__}").joinpath("data").joinpath(filename) if __package__ else Path(__file__).parent.parent / 'data'

def default_prefs() -> Path:
    return resources.files(f'{__package__}').joinpath('etc') if __package__ else Path(__file__).parent.parent / 'etc'

def read_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()

def pkg_path() -> Path:
    if __package__: return resources.files(f'{__package__}')
    else: return Path(