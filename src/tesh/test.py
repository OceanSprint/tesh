"""Run testable sessions line-by-line and assert the output."""

from pathlib import Path
from tesh.extract import Block
from tesh.extract import get_prompt_regex
from tesh.extract import ShellSession

import fnmatch
import os
import pexpect
import re
import sys


def test(filename: str, session: ShellSession, verbose: bool, debug: bool) -> None:
    """Run testable sessions in a pexpect shell."""
    with Path(filename).parent:
        shell = pexpect.spawn(
            "bash --norc --noprofile",
            env={"PS1": "$ ", "PATH": os.environ["PATH"], "HOME": os.getcwd()},
        )
        shell.expect(r"\$ ")
        if session.setup:
            shell.sendline("source " + session.setup)
            shell.expect(get_prompt_regex(session))
        for index, block in enumerate(session.blocks):
            if verbose:
                print(":")
                print("       Command:", block.command)
                print("       Output:", block.output)

            expected_output = "\n".join(block.output)

            shell.sendline(block.command)
            shell.expect(re.escape(block.command))

            # we expect the prompt of the next command unless there's no more
            if index + 1 < len(session.blocks):
                prompt = session.blocks[index + 1].prompt
            else:
                prompt = session.blocks[index].prompt
            try:
                shell.expect(re.escape(prompt))

            # This is tested in test_timeout but coverage doesn't catch it because
            # it is executed in a subshell
            except pexpect.exceptions.TIMEOUT:  # pragma: no cover
                print("❌ Timed out after 30s")  # noqa: ENC100
                print()
                print("         Command:", block.command)
                print("         Output:")
                print(shell.before.decode("utf-8").strip().replace("\r\n", "\n"))
                if debug:
                    invoke_debug(shell, block)
                else:
                    sys.exit(1)

            expected_match = (
                expected_output.replace("*", "[*]")
                .replace("?", "[?]")
                .replace("...", "*")
            )
            actual_output = shell.before.decode("utf-8").strip().replace("\r\n", "\n")

            # trim whitespace in every line
            expected_output = "\n".join(
                [line.rstrip() for line in expected_output.split("\n")]
            )
            actual_output = "\n".join(
                [line.rstrip() for line in actual_output.split("\n")]
            )

            if not fnmatch.fnmatch(actual_output, expected_match):
                print("❌ Failed")  # noqa: ENC100
                print("         Command:", block.command)
                print()
                print("         Expected:")
                print(expected_output)
                print("         Got:")
                print(actual_output)

                # This is tested in test_debug but coverage doesn't catch it because
                # it is executed in a subshell
                if debug:  # pragma: no cover
                    invoke_debug(shell, block)
                else:
                    sys.exit(1)

            # handle exit codes
            shell.sendline("echo $?")
            shell.expect("echo [$][?]")
            shell.expect(re.escape(prompt))
            exitcode = int(shell.before.decode("utf-8").strip())
            if session.exitcodes and exitcode != session.exitcodes[index]:
                print("❌ Failed")  # noqa: ENC100
                print("         Command:", block.command)
                print()
                print("         Expected exit code:", session.exitcodes[index])
                print("         Got exit code:", exitcode)
                if debug:  # pragma: no cover
                    invoke_debug(shell, block)
                else:
                    sys.exit(1)


# This is tested in test_debug but coverage doesn't catch it because
# it is executed in a subshell
def invoke_debug(shell: pexpect.spawn, block: Block) -> None:  # pragma: no cover
    """Take the user to a debug shell."""
    print()
    print("Taking you into the shell ...")
    print()
    print(block.prompt, end="")
    shell.interact()


def write_fixtures(session: ShellSession) -> None:
    """Dump code block into a file."""
    for fixture in session.fixtures:
        # TODO: support directories
        with open(fixture.filename, "w") as f:
            f.write(fixture.contents)
