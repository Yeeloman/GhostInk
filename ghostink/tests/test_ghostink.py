import pytest
import json
from GhoslInk.ghostink import GhostInk

# Initialize a GhostInk instance for tests


@pytest.fixture
def ghostink():
    return GhostInk()


def test_initialization(ghostink):
    assert ghostink.title == "GhostInk"
    assert ghostink.project_root == "."
    assert ghostink.etchings == set()


def test_inkdrope(ghostink):
    ghostink.inkdrop("My first etch", GhostInk.mode.DEBUG)
    assert len(ghostink.etchings) == 1


def test_inkdrop_object(ghostink):
    ghostink.inkdrop({"etch": "Check this"}, GhostInk.mode.TODO)
    assert len(ghostink.etchings) == 1

    etch_text = list(ghostink.etchings)[0][1]
    assert etch_text == json.dumps({"etch": "Check this"}, indent=4)


def test_whisper_filtered_etchings(ghostink, capsys):
    ghostink.inkdrop("etch 1", GhostInk.mode.DEBUG)
    ghostink.inkdrop("etch 2", GhostInk.mode.INFO)

    ghostink.whisper(mode_mask=GhostInk.mode.DEBUG)  # Print only DEBUG etchings

    captured = capsys.readouterr()
    assert "etch 1" in captured.out
    assert "etch 2" not in captured.out  # Ensure other etchings are not printed


def test_format_etch_from_object_dict(ghostink):
    formatted = ghostink._format_etch_from_object({"key": "value"})
    assert formatted == json.dumps({"key": "value"}, indent=4)


def test_format_etch_from_object_list(ghostink):
    formatted = ghostink._format_etch_from_object(["item1", "item2"])
    assert formatted == "item1, item2"


def test_format_etch_from_object_set(ghostink):
    formatted = ghostink._format_etch_from_object({"item1", "item2"})
    # Sets are unordered
    assert formatted == "{item1, item2}" or formatted == "{item2, item1}"


def test_format_etch_from_object_other(ghostink):
    formatted = ghostink._format_etch_from_object(12345)
    assert formatted == "12345"


if __name__ == "__main__":
    pytest.main()
