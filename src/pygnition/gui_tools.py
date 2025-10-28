import os
from pathlib import Path
import subprocess

def zenity_available():
    return (
        os.environ.get("DISPLAY")
        and subprocess.run(["which", "zenity"], capture_output=True).returncode == 0
    )

def choose_file(
    title="Select a file",
    directory=False,
    multiple=False,
    save=False,
    confirm_overwrite=True,
    initial_path=None,
    filters=None,
    check_existence=True,
    relative_path=False,
    create_dirs=True,
    always_list=False,
    single_path=False,
):
    """
    Open a Zenity file chooser dialog and return selected file path(s).

    Falls back to command-line input if Zenity is not available
    or if no display environment is present.

    Parameters
    ----------
    title : str
        Window title for the dialog.
    directory : bool
        If True, choose a directory instead of a file.
    multiple : bool
        If True, allow multiple selections.
    save : bool
        If True, show a 'Save As' dialog instead of 'Open File'.
    confirm_overwrite : bool
        If True, ask for confirmation before overwriting (used with save=True).
    initial_path : str | Path | None
        Optional starting path (directory or file name).
    filters : list[tuple[str, str]] | None
        A list of (name, pattern) pairs.
    check_existence : bool
        If True, verify existence (open mode) or warn/auto-create (save mode).
    relative_path : bool
        If True, returned paths are relative to current working directory.
    create_dirs : bool
        If True and save=True, auto-create parent directories if missing.
    always_list : bool
        If True, always return a list of Path objects, even for single selection.
    single_path : bool
        If True, always return a single Path (first item if multiple selected).
        Overrides `always_list`.

    Returns
    -------
    Path | list[Path] | None
        A Path object, or list of Paths, or None if user cancels.

    ISSUE: Appears to change the current working directory.
        Workaround seems to be to declare CWD global when the project starts
        and change back to it at the end of any function that calls this one.

            2025-10-27: Added `@cwd_mover`. There are a lot of return statements.
    """

    def ensure_valid_path(p):
        if not check_existence:
            return True
        if save:
            if p.exists() and confirm_overwrite:
                ans = input(f"⚠️  '{p}' exists. Overwrite? [y/N]: ").strip().lower()
                return ans == "y"
            if create_dirs and not p.parent.exists():
                try:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    print(f"📂 Created parent directories for '{p}'")
                except Exception as e:
                    print(f"❌ Failed to create directories: {e}")
                    return False
            return True
        else:
            if not p.exists():
                print(f"❌ File or directory not found: {p}")
                return False
            return True

    def finalize_path(p):
        p = p.expanduser()
        return p.relative_to(Path.cwd()) if relative_path else p.resolve()

    # --- Zenity GUI ---
    if zenity_available():
        cmd = ["zenity", "--file-selection", f"--title={title}"]
        if directory:
            cmd.append("--directory")
        if multiple:
            cmd.extend(["--multiple", "--separator=|"])
        if save:
            cmd.append("--save")
            if confirm_overwrite:
                cmd.append("--confirm-overwrite")
        if initial_path:
            cmd.append(f"--filename={Path(initial_path).expanduser()}")
        if filters:
            for name, pattern in filters:
                cmd.extend(["--file-filter", f"{name} ({pattern}) | {pattern}"])

        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        output = result.stdout.strip()
        if not output:
            return [] if always_list else None

        paths = [Path(p) for p in output.split("|")] if multiple else [Path(output)]
        valid = [finalize_path(p) for p in paths if ensure_valid_path(p)]

    # --- CLI fallback ---
    else:
        print(f"\n[Zenity not available or no display detected]\n{title}")
        if multiple:
            raw = input("Enter one or more paths (separated by '|'): ").strip()
            if not raw:
                return [] if always_list else None
            paths = [Path(p.strip()).expanduser() for p in raw.split("|")]
            valid = [finalize_path(p) for p in paths if ensure_valid_path(p)]
        else:
            raw = input("Enter a file path (or leave blank to cancel): ").strip()
            if not raw:
                return [] if always_list else None
            p = Path(raw).expanduser()
            valid = [finalize_path(p)] if ensure_valid_path(p) else []

    if not valid:
        return [] if always_list else None

    if single_path:
        return valid[0]

    if multiple or always_list:
        return valid

    return valid[0]

if __name__ == '__main__':
    print(f'File(s) chosen: {choose_file()}')