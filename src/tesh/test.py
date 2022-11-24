"""Run testable sessions line-by-line and assert the output."""

from pathlib import Path
from tesh.extract import ShellSession

import fnmatch
import pexpect
import sys


def test(filename: str, session: ShellSession, verbose: bool) -> None:
    """Run testable sessions in a pexpect shell."""
    with Path(filename).parent:
        shell = pexpect.spawn('env -i PS1="$ " bash --norc --noprofile')
        shell.expect(r"\$ ")
        # TODO: this doesn't really work, fix and uncomment
        # if session.setup:
        #     shell.sendline(session.setup)
        #     shell.expect(r"\$ ")
        for index, block in enumerate(session.blocks):
            if verbose:
                print("      ", block)

            expected_output = "\n".join(block.output)

            # if "DEBUG" in expected_output:
            #     print()
            #     print("$ ", end="")
            #     shell.send(block.command)
            #     shell.interact()

            shell.sendline(block.command)

            shell.expect(block.command)
            shell.expect(r"\$ ")

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
