"""Tests for the extract.py module."""

from tesh.extract import Block
from tesh.extract import parse_exitcodes
from tesh.extract import ShellSession

import pytest


def test_parse_exitcodes() -> None:
    """Test edge cases with parsing exitcodes spec."""

    # happy path
    assert parse_exitcodes("0 1 0") == [0, 1, 0]

    # whitespace
    assert parse_exitcodes(" 0   1 0 ") == [0, 1, 0]

    # non-integers
    with pytest.raises(ValueError) as error:
        parse_exitcodes(" 0   foo 0 ")

    assert str(error.value) == "invalid literal for int() with base 10: 'foo'"


def test_Block() -> None:
    """Test edge cases with the Block dataclass."""

    # full data
    Block(command="foo", output=["bar", "baz"])

    # minimal data
    Block("foo")


def test_ShellSession() -> None:
    """Test edge cases with the ShellSession dataclass."""

    # full data
    ShellSession(
        lines=["foo", "bar", "baz"],
        blocks=[Block("foo")],
        id_="str",
        setup="foo.sh",
        exitcodes=[0, 1, 2],
    )

    # minimal data
    ShellSession(lines=["foo", "bar", "baz"], blocks=[Block("foo")], id_="str")
