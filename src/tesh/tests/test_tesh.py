"""Tests for main tesh runner."""

from click.testing import CliRunner
from tesh import tesh

import pexpect


def test_version() -> None:
    """Test printing the current version."""
    runner = CliRunner()
    result = runner.invoke(tesh, "--version")

    assert result.exit_code == 0
    assert "tesh, version 0.3.0\n" == result.output


def test_empty_folder() -> None:
    """Test pointing tesh to an empty folder."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/empty_folder")

    assert result.exit_code == 0
    assert "" == result.output


def test_no_codeblocks() -> None:
    """Test pointing tesh to a Markdown file with no codeblocks."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/no_codeblocks.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/no_codeblocks.md
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_simple() -> None:
    """Test pointing tesh to a simple Markdown file."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/folder/simple.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/folder/simple.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_verbose() -> None:
    """Test verbose output."""
    runner = CliRunner()
    result = runner.invoke(tesh, "--verbose src/tesh/tests/fixtures/folder/simple.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/folder/simple.md
  ✨ Running foo  :
       Command: echo "foo ✨"
       Output: ['foo ✨']
✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_folder() -> None:
    """Test pointing tesh to a folder and test that it reads the contained file."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/folder")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/folder/simple.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_multiple_codeblocks() -> None:
    """Test pointing tesh to a Markdown file with multiple codeblocks."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/multiple_codeblocks.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/multiple_codeblocks.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_fail() -> None:
    """Test pointing tesh to a failing Markdown file."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/fail.md")

    assert result.exit_code == 1

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/fail.md
  ✨ Running foo  ❌ Failed
         Command: echo "foo"

         Expected:
bar
         Got:
foo
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_debug() -> None:  # pragma: no cover
    """Test dropping into an interactive shell on error."""
    shell = pexpect.spawn("tesh src/tesh/tests/fixtures/debug.md", encoding="utf-8")
    shell.expect("Taking you into the shell ...")

    assert isinstance(shell.before, str)
    assert "✨ Running foo  ❌ Failed" in shell.before


def test_timeout() -> None:  # pragma: no cover
    """Test dropping into an interactive shell on timeout."""
    shell = pexpect.spawn("tesh src/tesh/tests/fixtures/timeout.md", encoding="utf-8")
    shell.expect("Taking you into the shell ...", timeout=60)

    assert isinstance(shell.before, str)
    assert "✨ Running foo  ❌ Timed out after 1s" in shell.before


def test_exitcodes() -> None:
    """Test pointing tesh to a Markdown file using exitcodes."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/exitcodes.md")

    assert result.exit_code == 1

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/exitcodes.md
  ✨ Running foo  ✅ Passed
  ✨ Running bar  ❌ Failed
         Command: false

         Expected exit code: 0
         Got exit code: 1
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_exitcodes_multiple_blocks() -> None:
    """Test failure if not all blocks specify exitcodes."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/exitcodes_multipleblocks.md")

    assert result.exit_code == 1

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/exitcodes_multipleblocks.md
  ✨ Running foo  ❌ Failed
     If you're using exit codes for a session, you must specify them for all commands.
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_setup() -> None:
    """Test using tesh-setup to prepare the session before running examples."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/setup.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/setup.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_setup_nonexistent_file() -> None:
    """Test tesh-setup failure if file does not exist."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/setup_fail.md")

    assert result.exit_code == 1

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/setup_fail.md
❌ Failed
     Setup file does not exist: src/tesh/tests/fixtures/does_not_exist.sh
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_fixture() -> None:
    """Test using tesh-fixture to dump a code block into a file for later use."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/fixture.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/fixture.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_prompt() -> None:
    """Test using tesh-ps1 to detect a custom PS1 prompt."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/prompt.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/prompt.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_long_commands() -> None:
    """Test lengthy commands, which can be truncated if they're too long."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/long_command.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/long_command.md
  ✨ Running long-cmds  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_multiline_command() -> None:
    """Test using `> ` to extend a command across more than one line."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/multiline_command.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/multiline_command.md
  ✨ Running readme-example  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_wildcards() -> None:
    """Test using ... to ignore parts of the output."""
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/wildcards.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/wildcards.md
  ✨ Running foo  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output


def test_whitespace() -> None:
    """Test code blocks with whitespace.

    Both whitespace in command output, and indented code blocks.
    """
    runner = CliRunner()
    result = runner.invoke(tesh, "src/tesh/tests/fixtures/whitespace.md")

    assert result.exit_code == 0

    # fmt: off
    expected = (
"""
📄 Checking src/tesh/tests/fixtures/whitespace.md
  ✨ Running non-indented-block  ✅ Passed
  ✨ Running indented-block  ✅ Passed
  ✨ Running extra-trailing-whitespace  ✅ Passed
"""
    ).lstrip("\n")
    # fmt: on

    assert expected == result.output
