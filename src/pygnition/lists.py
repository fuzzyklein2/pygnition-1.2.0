from .startmeup import *

@auto_doc()
def first_after_last_digits(strings: list[str]) -> str | None:
    """
        Return the `str` directly after the last `str` containing only digits
        in `strings`.
    """
    last_digit_index = None
    for i, s in enumerate(strings):
        if s.isdigit():
            last_digit_index = i
    if last_digit_index is not None and last_digit_index + 1 < len(strings):
        return strings[last_digit_index + 1]
    return None

