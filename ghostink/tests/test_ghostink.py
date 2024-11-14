import pytest
import os
from ghostink import GhostInk


# Initial setup for testing the GhostInk class
@pytest.fixture
def ghostink_instance():
    return GhostInk(title="TestInstance", project_root="test_project")


# Teardown: clean up generated logs after tests
@pytest.fixture(scope="function", autouse=True)
def clean_up_logs():
    yield
    if os.path.exists("test_project/.ghost"):
        for file in os.listdir("test_project/.ghost"):
            os.remove(os.path.join("test_project/.ghost", file))
        os.rmdir("test_project/.ghost")


def test_initialization():
    ink = GhostInk(title="TestTitle", project_root="test_root")
    assert ink.title == "TestTitle"
    assert ink.project_root == "test_root"
    assert ink.entries == set()


def test_haunt(capsys):
    ink = GhostInk()
    ink.haunt("Testing haunt message")
    captured = capsys.readouterr()
    assert "Testing haunt message" in captured.out
    assert "haunt" in captured.out


def test_inkdrop_basic(ghostink_instance):
    ghostink_instance.inkdrop("Simple test entry")
    assert any("Simple test entry" in entry[1]
               for entry in ghostink_instance.entries)


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


# def test_format_tags(ghostink_instance):
#     tags = ["tag1", " tag2", "#tag3"]
#     formatted = ghostink_instance._format_tags(tags)
#     assert "#tag1" in formatted
#     assert "#tag2" in formatted
#     assert "#tag3" not in formatted  # Excludes tags with `#`


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
    ghost_dir_path = os.path.join(ghostink_instance.project_root, ".ghost")
    assert os.path.exists(ghost_dir_path)
    ghostink_instance.clean()
    assert not os.path.exists(ghost_dir_path)


# TODO test for the logger
if __name__ == "__main__":
    pytest.main()
