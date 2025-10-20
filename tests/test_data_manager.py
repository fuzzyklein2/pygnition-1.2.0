import pytest
import tempfile
from pathlib import Path
import time
from pygnition.data import PackageData

# --- Fixture: enable debug mode for tests ---
@pytest.fixture(autouse=True)
def enable_debug(monkeypatch):
    monkeypatch.setenv("PYGNITION_DEBUG", "1")
    yield
    monkeypatch.delenv("PYGNITION_DEBUG", raising=False)

# --- Fixture: temporary data directory ---
@pytest.fixture
def temp_data_dir():
    tmpdir = Path(tempfile.mkdtemp(prefix="pkgdata_test_"))
    datadir = tmpdir / "data"
    datadir.mkdir()

    # Base files
    (datadir / "author.txt").write_text("Arthur Conan Doyle\n")
    (datadir / "description.txt").write_text("A brilliant mind, a curious machine.\n")
    (datadir / "binary.dat").write_bytes(b"\x00\x01\x02\x03")

    yield datadir

    import shutil
    shutil.rmtree(tmpdir)

# --- Fixture: PackageData instance using temp directory ---
@pytest.fixture
def data_manager(temp_data_dir):
    # Just point PackageData to the temp directory
    return PackageData(base_dir=temp_data_dir)

# --- Tests ---

def test_text_read(data_manager):
    text = data_manager.get("author.txt")
    assert text.strip() == "Arthur Conan Doyle"

def test_bytes_read(data_manager):
    b = data_manager.get("binary.dat", mode="bytes")
    assert b == b"\x00\x01\x02\x03"

def test_default_on_missing(data_manager):
    val = data_manager.get("nonexistent.txt", default="default_value")
    assert val == "default_value"

def test_auto_reload_single_file(data_manager, temp_data_dir):
    path = temp_data_dir / "author.txt"
    original = data_manager.get("author.txt")
    assert original.strip() == "Arthur Conan Doyle"

    time.sleep(1)
    path.write_text("Sherlock Holmes\n")
    updated = data_manager.get("author.txt")
    assert updated.strip() == "Sherlock Holmes"

def test_list_and_glob(data_manager, temp_data_dir):
    (temp_data_dir / "notes.txt").write_text("Some notes\n")
    (temp_data_dir / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (temp_data_dir / "config.yaml").write_text("setting: true\n")

    txt_files = list(data_manager.list("*.txt"))
    txt_names = [f.name for f in txt_files]
    for name in ["author.txt", "description.txt", "notes.txt"]:
        assert name in txt_names
    assert "config.yaml" not in txt_names

    all_files = list(data_manager.list("*"))
    all_names = [f.name for f in all_files]
    for expected in ["author.txt", "description.txt", "notes.txt", "binary.dat", "image.png", "config.yaml"]:
        assert expected in all_names

def test_auto_reload_multiple_files(data_manager, temp_data_dir):
    a1 = data_manager.get("author.txt")
    b1 = data_manager.get("binary.dat", mode="bytes")
    d1 = data_manager.get("description.txt")

    time.sleep(1)
    (temp_data_dir / "author.txt").write_text("Dr. Watson\n")
    (temp_data_dir / "binary.dat").write_bytes(b"\x10\x20\x30")
    (temp_data_dir / "description.txt").write_text("Updated description\n")

    a2 = data_manager.get("author.txt")
    b2 = data_manager.get("binary.dat", mode="bytes")
    d2 = data_manager.get("description.txt")

    assert a2.strip() == "Dr. Watson"
    assert b2 == b"\x10\x20\x30"
    assert d2.strip() == "Updated description"

def test_nested_directories_recursive_glob(data_manager, temp_data_dir):
    nested_dir = temp_data_dir / "subdir" / "inner"
    nested_dir.mkdir(parents=True)

    (nested_dir / "nested1.txt").write_text("Nested file 1")
    (nested_dir / "nested2.txt").write_text("Nested file 2")
    (nested_dir / "binary_nested.dat").write_bytes(b"\xDE\xAD\xBE\xEF")

    txt_files = list(data_manager.list("**/*.txt"))
    txt_names = [f.name for f in txt_files]
    for name in ["author.txt", "description.txt", "nested1.txt", "nested2.txt"]:
        assert name in txt_names

    all_files = list(data_manager.list("**/*"))
    all_names = [f.name for f in all_files]
    expected_files = [
        "author.txt", "description.txt", "binary.dat",
        "nested1.txt", "nested2.txt", "binary_nested.dat"
    ]
    for name in expected_files:
        assert name in all_names

    assert data_manager.get("subdir/inner/nested1.txt").strip() == "Nested file 1"
    assert data_manager.get("subdir/inner/nested2.txt").strip() == "Nested file 2"
    assert data_manager.get("subdir/inner/binary_nested.dat", mode="bytes") == b"\xDE\xAD\xBE\xEF"
