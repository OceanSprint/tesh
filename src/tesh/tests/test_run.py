"""Tests for main tesh runner."""

from click.testing import CliRunner
from tesh import run


def test_version() -> None:
    """Test printing the current version."""
    runner = CliRunner()
    result = runner.invoke(run, "--version")

    assert result.exit_code == 0
    assert "run, version 0.1.0\n" == result.output  # TODO: run -> tesh


def test_empty_folder() -> None:
    """Test pointing tesh to an empty folder."""
    runner = CliRunner()
    result = runner.invoke(run, "src/tesh/tests/fixtures/empty_folder")

    assert result.exit_code == 0
    assert "" == result.output


def test_no_codeblocks() -> None:
    """Test pointing tesh to a Markdown file with no codeblocks."""
    runner = CliRunner()
    result = runner.invoke(run, "src/tesh/tests/fixtures/no_codeblocks.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/no_codeblocks.md
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_multiple_codeblocks() -> None:
    """Test pointing tesh to a Markdown file with multiple codeblocks."""
    runner = CliRunner()
    result = runner.invoke(run, "src/tesh/tests/fixtures/multiple_codeblocks.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/multiple_codeblocks.md
  ✨ Running foo
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_folder() -> None:
    """Test pointing tesh to a folder and test that it reads the contained file."""
    runner = CliRunner()
    result = runner.invoke(run, "src/tesh/tests/fixtures/folder")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/folder/contained.md
  ✨ Running foo
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output