import tempfile
from pathlib import Path

from envcheck.core import compare, parse_env


def test_parse_env():
    f = Path("_test_env")
    f.write_text("""
# comment
FOO=bar
BAZ=qux
EMPTY=
QUOTED="hello world"
""")
    try:
        result = parse_env(f)
        assert result == {"FOO": "bar", "BAZ": "qux", "EMPTY": "", "QUOTED": "hello world"}
    finally:
        f.unlink()


def test_compare_all_match():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        base = Path(td) / ".env.example"
        prod = Path(td) / ".env"
        base.write_text("A=1\nB=2\n")
        prod.write_text("A=1\nB=2\n")
        diffs = compare(base, prod)
        assert diffs == []


def test_compare_missing_key():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        base = Path(td) / ".env.example"
        prod = Path(td) / ".env"
        base.write_text("A=1\nB=2\n")
        prod.write_text("A=1\n")
        diffs = compare(base, prod)
        assert len(diffs) == 1
        assert diffs[0].key == "B"
        assert diffs[0].issue == "missing"


def test_compare_extra_key():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        base = Path(td) / ".env.example"
        prod = Path(td) / ".env"
        base.write_text("A=1\n")
        prod.write_text("A=1\nB=2\n")
        diffs = compare(base, prod)
        assert len(diffs) == 1
        assert diffs[0].key == "B"
        assert diffs[0].issue == "extra"


def test_compare_mismatch():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        base = Path(td) / ".env.example"
        prod = Path(td) / ".env"
        base.write_text("A=1\n")
        prod.write_text("A=2\n")
        diffs = compare(base, prod)
        assert len(diffs) == 1
        assert diffs[0].key == "A"
        assert diffs[0].issue == "mismatch"


def test_compare_multiple_files():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        base = Path(td) / ".env.example"
        staging = Path(td) / ".env.staging"
        prod = Path(td) / ".env.prod"
        base.write_text("A=1\nB=2\nC=3\n")
        staging.write_text("A=1\nB=99\n")
        prod.write_text("A=1\nB=2\nC=4\n")
        diffs = compare(base, staging, prod)
        assert len(diffs) == 3  # B missing in staging, B mismatch staging, C mismatch prod
