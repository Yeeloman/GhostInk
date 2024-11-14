import pytest
from typer.testing import CliRunner
from ghostink.cli import app

runner = CliRunner()

@pytest.fixture
def setup_env(monkeypatch, tmp_path):
    """Set up the environment variable and temporary file for each test."""
    ghost_path = tmp_path / ".ghost"
    ghost_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("GHOSTINK", str(ghost_path))
    return ghost_path

def test_version(setup_env):
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert "Ghosty" in result.output
    
# def test_show_path(setup_env):
#     result = runner.invoke(app, ["-P"])
#     assert result.exit_code == 0
#     expected_output = f".ghost dir in: {setup_env}"
#     assert expected_output in result.output
