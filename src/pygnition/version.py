# pygnition/version.py
import re
import subprocess

class Version(str):
    """Semantic-style version string with optional prefix/suffix.
    
    Format:
        [v]MAJOR.MINOR.PATCH[suffix]
    where suffix ∈ {"a", "b", "c"} or empty.
    
    'a' > 'b' > 'c' > '' in sort order.
    """

    _pattern = re.compile(
        r'^(?P<prefix>v)?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>[abc]?)$'
    )

    def __new__(cls, version: str):
        match = cls._pattern.match(version)
        if not match:
            raise ValueError(f"Invalid version string: {version!r}")

        obj = super().__new__(cls, version)
        obj.has_v_prefix = bool(match.group('prefix'))
        obj.major = int(match.group('major'))
        obj.minor = int(match.group('minor'))
        obj.patch = int(match.group('patch'))
        obj.suffix = match.group('suffix') or ""
        return obj

    def __repr__(self):
        return f"Version({str(self)!r})"

    def __str__(self):
        prefix = "v" if self.has_v_prefix else ""
        return f"{prefix}{self.major}.{self.minor}.{self.patch}{self.suffix}"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._cmp_tuple() == other._cmp_tuple()

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._cmp_tuple() < other._cmp_tuple()

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def _cmp_tuple(self):
        # Reversed suffix order: a > b > c > ""
        suffix_order = {"": 0, "c": 1, "b": 2, "a": 3}
        return (self.major, self.minor, self.patch, suffix_order[self.suffix])

    @classmethod
    def is_valid(cls, s: str) -> bool:
        """Return True if `s` is a valid version string."""
        return bool(cls._pattern.match(s))

    @classmethod
    def from_git(cls, repo_path: str = ".") -> "Version":
        """Try to get the latest Git tag from the repo and return as Version."""
        try:
            tag = (
                subprocess.check_output(
                    ["git", "-C", repo_path, "describe", "--tags", "--abbrev=0"],
                    stderr=subprocess.DEVNULL,
                )
                .decode()
                .strip()
            )
            return cls(tag)
        except Exception:
            return cls("v0.0.1")  # default fallback
