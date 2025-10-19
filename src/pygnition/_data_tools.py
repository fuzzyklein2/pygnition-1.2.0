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

