from datetime import date
import inspect
from pathlib import Path

def auto_doc(heading_template=None):
    """
    Decorator that preserves the original function docstring and
    appends auto-generated Markdown tables for parameters and return types.
    Optionally adds a heading template at the top.
    """
    def decorator(func):
        sig = inspect.signature(func)
        orig_doc = func.__doc__ or ""
        lines = []

        # Optional heading template
        if heading_template:
            VERSION = Path(__file__).parent.parent.name.split('-')[-1]
            lines.append(heading_template.format(
                name=func.__name__,
                version=VERSION,
                date=date.today().isoformat()
            ))
            lines.append("")  # blank line

        # Include original docstring
        if orig_doc.strip():
            lines.append(orig_doc.strip())
            lines.append("")  # blank line

        # Auto-generate parameter table
        if sig.parameters:
            lines.append("#### Parameters\n")
            lines.append("Name | Type(s) | Description")
            lines.append("--- | --- | ---")

            for name, param in sig.parameters.items():
                annot = param.annotation
                if annot == inspect.Parameter.empty:
                    annot_str = "Any"
                elif isinstance(annot, type):
                    annot_str = annot.__name__
                else:
                    annot_str = str(annot)

                default = (
                    f" *(default={param.default})*"
                    if param.default != inspect.Parameter.empty
                    else ""
                )

                # We don't have descriptions from code, so leave blank
                lines.append(f"{name} | {annot_str}{default} | ")

            lines.append("")  # blank line

        # Auto-generate return info
        return_annot = sig.return_annotation
        if return_annot == inspect.Signature.empty:
            return_annot_str = "Any"
        elif isinstance(return_annot, type):
            return_annot_str = return_annot.__name__
        else:
            return_annot_str = str(return_annot)

        lines.append("#### Returns\n")
        lines.append("Type | Description")
        lines.append("--- | ---")
        lines.append(f"{return_annot_str} | ")

        func.__doc__ = "\n".join(lines)
        return func

    return decorator

# Example usage
@auto_doc("Function: {name} (module version {version}, generated {date})")
def add(a: int, b: int = 0) -> int:
    """Add two numbers together in a friendly way."""
    return a + b


@auto_doc()
def greet(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # print(add.__doc__)
    # print("\n" + "-" * 40 + "\n")
    # print(greet.__doc__)
    import doctest
    doctest.testmod()