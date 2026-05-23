from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Diff:
    key: str
    issue: str  # "missing" | "extra" | "mismatch"
    values: dict[str, str | None]


def parse_env(path: Path) -> dict[str, str]:
    """Parse a .env file, returning key-value pairs. Skips comments and blank lines."""
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" in stripped:
            key, _, value = stripped.partition("=")
            result[key.strip()] = value.strip().strip("\"'")
    return result


def compare(base: Path, *others: Path) -> list[Diff]:
    """Compare .env files. base is the reference (e.g. .env.example)."""
    base_vars = parse_env(base)
    base_keys = set(base_vars)
    diffs: list[Diff] = []
    names = [base.name] + [o.name for o in others]

    for i, other in enumerate(others):
        other_vars = parse_env(other)
        other_keys = set(other_vars)
        label = other.name

        for key in sorted(base_keys - other_keys):
            diffs.append(Diff(key=key, issue="missing",
                             values={base.name: base_vars[key], label: None}))

        for key in sorted(other_keys - base_keys):
            diffs.append(Diff(key=key, issue="extra",
                             values={base.name: None, label: other_vars[key]}))

        for key in sorted(base_keys & other_keys):
            if base_vars[key] != other_vars[key]:
                diffs.append(Diff(key=key, issue="mismatch",
                                 values={base.name: base_vars[key], label: other_vars[key]}))

    return diffs
