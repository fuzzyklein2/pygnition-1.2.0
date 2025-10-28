def is_valid_data_line(s:str)->bool:
    """
        Return True if the line does not begin with a comment
        and False if it does

        ### Example Usage

        >>> is_valid_data_line("# starts with comment")
        False

        >>> is_valid_data_line("anything else")
        True
    """
    if s.startswith('#') or s.isspace() or not s: return False
    return True

def get_data(p: Path, s: str) -> str:
    """ Get the contents of the file p / s.txt """
    data_file = p / f'{s}.txt'
    try:
        return data_file.read_text()
    except FileNotFoundError:
        return ''