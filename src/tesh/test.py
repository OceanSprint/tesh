"""Run testable sessions line-by-line and assert the output."""

from pathlib import Path
from tesh.extract import ShellSession

import fnmatch
import os
import pexpect
import sys


def test(filename: str, session: ShellSession, verbose: bool) -> None:
    """Run testable sessions in a pexpect shell."""
    with Path(filename).parent:
        shell = pexpect.spawn(
            "bash --norc --noprofile",
            env={"PS1": "$ ", "PATH": os.environ["PATH"]},
        )
        shell.expect(r"\$ ")
        if session.setup:
            shell.sendline("source " + session.setup)
            shell.expect(r"\$ ")
        for index, block in enumerate(session.blocks):
            if verbose:
                print()
                print("      Command: ", block.command)
                print("      Output: ", block.output)

            expected_output = "\n".join(block.output)

            # This is actually covered in test_debug() but coverage does not
            # detect it because the test spawns a sub-shell
            if "DEBUG" in expected_output:  # pragma: no cover
                print()
                print("$ ", end="")
                shell.send(block.command)
                shell.interact()

            shell.sendline(block.command)

            shell.expect(block.command.replace("$", r"\$"))

            shell.expect(r"\$ ")

            expected_match = (
                expected_output.strip()
                .replace("*", "[*]")
                .replace("?", "[?]")
                .replace("...", "*")
            )
            actual_output = shell.before.decode("utf-8").strip().replace("\r\n", "\n")

            expected_match = (
                expected_output.strip()
                .replace("*", "[*]")
                .replace("?", "[?]")
                .replace("...", "*")
            )
            actual_output = shell.before.decode("utf-8").strip().replace("\r\n", "\n")

            if not fnmatch.fnmatch(actual_output, expected_match):
                print("❌ Failed")  # noqa: ENC100
                print()
                print("         Expected:")
                print(expected_output)
                print("         Got:")
                print(actual_output)
                sys.exit(1)

            # handle exit codes
            shell.sendline("echo $?")
            shell.expect("echo [$][?]")
            shell.expect(r"\$ ")
            exitcode = int(shell.before.decode("utf-8").strip())
            if session.exitcodes and exitcode != session.exitcodes[index]:
                print("❌ Failed")  # noqa: ENC100
                print()
                print("         Expected exit code:", session.exitcodes[index])
                print("         Got exit code:", exitcode)
                sys.exit(1)


def write_fixtures(session: ShellSession) -> None:
    """Dump code block into a file."""
    for fixture in session.fixtures:
        # TODO: support directories
        with open(fixture.filename, "w") as f:
            f.write(fixture.contents)
