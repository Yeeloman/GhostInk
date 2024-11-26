import os
import pytest
import shutil
from pathlib import Path
from ghostink import GhostInk


# Initial setup for testing the GhostInk class
@pytest.fixture
def ghostink_instance():
    return GhostInk(title="TestInstance")


# Teardown: clean up generated logs after tests
@pytest.fixture(scope="function", autouse=True)
def clean_up_logs():
    yield
    base_path = Path("/home/yeeloman/.config/ghosty")
    test_root_path = base_path / "test_root" / "TestTitle"

    if test_root_path.exists():
        for file in os.listdir(test_root_path):
            file_path = test_root_path / file
            if file_path.is_file():
                os.remove(file_path)  # Remove individual files
            elif file_path.is_dir():
                shutil.rmtree(file_path)  # Remove directories recursively

        # After cleaning, remove the TestTitle directory itself
        if test_root_path.exists() and not os.listdir(test_root_path):  # Ensure empty
            os.rmdir(test_root_path)

        if test_root_path.parent.exists():
            os.rmdir(test_root_path.parent)


@pytest.fixture
def setup_env(monkeypatch):
    # Clear the GHOSTINK environment variable to test default behavior
    monkeypatch.delenv("GHOSTINK", raising=False)


def test_initialization_with_env_var(monkeypatch):
    # Set GHOSTINK to a custom value
    monkeypatch.setenv("GHOSTINK", ".")
    ink = GhostInk(title="TestTitle")

    assert ink.title == "TestTitle"
    assert ink.entries == set()


def test_initialization_without_env_var(setup_env):
    # Without GHOSTINK, it should use the provided project_root
    ink = GhostInk(title="TestTitle")

    assert ink.title == "TestTitle"
    assert ink.entries == set()


def test_haunt(capsys):
    ink = GhostInk()
    ink.haunt("Testing haunt message")
    captured = capsys.readouterr()
    assert "Testing haunt message" in captured.out
    assert "haunt" in captured.out


def test_inkdrop_basic(ghostink_instance):
    ghostink_instance.inkdrop("Simple test entry")
    assert any("Simple test entry" in entry[1] for entry in ghostink_instance.entries)


def test_inkdrop_dict_input(ghostink_instance):
    data = {"key": "value"}
    ghostink_instance.inkdrop(data)
    assert any(
        "key" in entry[1] and "value" in entry[1] for entry in ghostink_instance.entries
    )


def test_whisper(capsys, ghostink_instance):
    ghostink_instance.inkdrop("Debug message", shade=GhostInk.shade.DEBUG)
    ghostink_instance.inkdrop("Info message", shade=GhostInk.shade.INFO)
    ghostink_instance.whisper(filter_shade=GhostInk.shade.DEBUG)
    captured = capsys.readouterr()
    assert "Debug message" in captured.out
    assert "Info message" not in captured.out


def test_color_text(ghostink_instance):
    text = "Test"
    for shade in GhostInk.shade:
        colored_text = ghostink_instance._color_text(shade, text)
        assert text in colored_text


def test_get_relative_path(ghostink_instance):
    path, line, func = ghostink_instance._get_relative_path()
    assert isinstance(path, str)
    assert isinstance(line, int)
    assert isinstance(func, str)


def test_format_entry_from_object(ghostink_instance):
    # Test with dict
    dict_input = {"key": "value"}
    formatted = ghostink_instance._format_entry_from_object(dict_input)
    assert '"key": "value"' in formatted

    # Test with list
    list_input = [1, 2, 3]
    formatted = ghostink_instance._format_entry_from_object(list_input)
    assert "[\n    1,\n    2,\n    3\n]" in formatted

    # Test with custom object
    class CustomObj:
        def __init__(self):
            self.attr = "test"

    obj_input = CustomObj()
    formatted = ghostink_instance._format_entry_from_object(obj_input)
    assert '"attr": "test"' in formatted


def test_format_entry(ghostink_instance):
    entry_text = "Sample entry"
    formatted = ghostink_instance._format_entry(
        GhostInk.shade.INFO, entry_text, "file.py", 10, "test_func", ["tag"]
    )
    assert "Sample entry" in formatted
    assert "file.py" in formatted
    assert "(Ln:" in formatted
    assert "tag" in formatted


def test_clean(ghostink_instance):
    ghost_dir_path = Path(ghostink_instance.Group)
    assert ghost_dir_path.exists()
    ghostink_instance.clean()
    assert not os.path.exists(ghost_dir_path)


# TODO test for the logger
if __name__ == "__main__":
    pytest.main()
