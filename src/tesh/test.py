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


class NoANSIExpecter(pexpect.Expecter):
    """Custom Expecter to filter out ANSI escape code."""

    # regex for vt100 from https://stackoverflow.com/a/14693789/5008284
    ansi_escape = re.compile(r"(\x1B[@-_][0-?]*[ -/]*[@-~]|\\[\[\]])")

    def new_data(self, data: str) -> int:
        """Filter out ANSI escape code.

        And then call original `pexpect.Expecter.new_data` function.
        """
        data = self.ansi_escape.sub("", data)
        return pexpect.Expecter.new_data(self, data)


class spawn(pexpect.spawn):
    def expect_list(
        self,
        pattern_list: list[str],
        timeout: int = -1,
        searchwindowsize: int = -1,
        async_: bool = False,
        **kw: bool,
    ) -> int:
        """Use NoANSIExpecter to filter out ANSI escape code.

        We copied original `expect_list` function to be able to replace the
        Expecter.
        """
        if timeout == -1:
            timeout = self.timeout
        if "async" in kw:  # pragma: no cover
            async_ = kw.pop("async")
        if kw:  # pragma: no cover
            raise TypeError("Unknown keyword arguments: {}".format(kw))

        exp = NoANSIExpecter(
            self, pexpect.expect.searcher_re(pattern_list), searchwindowsize
        )
        if async_:  # pragma: no cover
            from pexpect._async import expect_async

            return expect_async(exp, timeout)
        else:
            return exp.expect_loop(timeout)


def test(filename: str, session: ShellSession, verbose: bool, debug: bool) -> None:
    """Run testable sessions in a pexpect shell."""
    with Path(filename).parent:
        shell = spawn(
            "bash --norc --noprofile",
            encoding="utf-8",
            env={"PS1": "$ ", "PATH": os.environ["PATH"], "HOME": os.getcwd()},
            # The (height, width) of the TTY commands run in. 24 is the default.
            # The width needs to be larger than the longest command, as
            # otherwise the command string gets truncated and the shell.expect
            # calls fail to match the the pattern's full command against the
            # truncated output.
            dimensions=(24, 1000),
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

            shell.sendline(block.command)
            for command_line in block.command.splitlines():
                shell.expect_exact(command_line + "\r\n")

            # we expect the prompt of the next command unless there's no more
            if index + 1 < len(session.blocks):
                prompt = session.blocks[index + 1].prompt
            else:
                prompt = session.blocks[index].prompt
            prompt = re.escape(prompt)
            prompt = prompt.replace("\\.\\.\\.", "(?=\\r\\n(?!.*\\r\\n)).*")
            try:
                shell.expect(prompt, timeout=session.timeout)

            # This is tested in test_timeout but coverage doesn't catch it because
            # it is executed in a subshell
            except pexpect.exceptions.TIMEOUT:  # pragma: no cover
                if session.long_running:
                    if index + 1 == len(session.blocks):
                        compare_outputs(shell, block, debug)
                        continue

                print(
                    "❌ Timed out after {timeout}s".format(  # noqa: ENC100
                        timeout=session.timeout
                    )
                )
                print()
                print("         Command:", block.command)
                print("         Output:")
                print(get_actual_output(shell))
                if debug:
                    invoke_debug(shell, block)
                else:
                    sys.exit(1)

            compare_outputs(shell, block, debug)

            # handle exit codes
            shell.sendline("echo $?")
            shell.expect("echo [$][?]")
            shell.expect(prompt)
            assert isinstance(shell.before, str)
            exitcode = int(shell.before.strip())
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


def get_actual_output(shell: spawn) -> str:
    """Massage shell output to be able to compare it."""
    assert isinstance(shell.before, str)
    actual_output = shell.before.rstrip().replace("\r\n", "\n")
    return "\n".join([line.rstrip() for line in actual_output.split("\n")])


def get_expected_output(block: Block) -> str:
    """Massage expected output to be able to compare it."""
    expected_output = (
        "\n".join(block.output)
        .replace("[", "[[]")
        .replace("*", "[*]")
        .replace("?", "[?]")
        .replace("...", "*")
    )
    # trim whitespace in every line
    return "\n".join([line.rstrip() for line in expected_output.split("\n")])


def compare_outputs(shell: spawn, block: Block, debug: bool) -> None:
    """Compare expected and the actual output and fail if they don't match."""
    actual_output = get_actual_output(shell)
    expected_output = get_expected_output(block)

    if not fnmatch.fnmatch(actual_output, expected_output):
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


# This is tested in test_debug but coverage doesn't catch it because
# it is executed in a subshell
def invoke_debug(shell: spawn, block: Block) -> None:  # pragma: no cover
    """Take the user to a debug shell."""
    print()
    print("Taking you into the shell ...")
    print()
    print("Enter `!!` to rerun the last command.")
    print()
    print(block.prompt, end="")
    shell.interact()


def write_fixtures(session: ShellSession) -> None:
    """Dump code block into a file."""
    for fixture in session.fixtures:
        # TODO: support directories
        with open(fixture.filename, "w") as f:
            f.write(fixture.contents)
