import pexpect
import os
import sys
import fnmatch
from pathlib import Path

def test(filename, session, verbose: bool):
    with Path(filename).parent:
        shell = pexpect.spawn('env -i PS1="$ " bash --norc --noprofile')
        shell.expect("\$ ")
        if session.setup:
            shell.sendline(session.setup)
            shell.expect("\$ ")
        for i, block in enumerate(session.blocks):
            if verbose:
                print("      ", block)

            expected_output = "\n".join(block.output)

            if "DEBUG" in expected_output:
                print()
                print("$ ", end="")
                shell.send(block.command)
                shell.interact()

            shell.sendline(block.command)

            shell.expect(block.command)
            shell.expect("\$ ")


            expected_match = expected_output.strip().replace("*", "[*]").replace("?", "[?]").replace("...", "*")
            actual_output = shell.before.decode("utf-8").strip().replace('\r\n', '\n')


            if not fnmatch.fnmatch(actual_output, expected_match):
                print("❌ Failed")
                print()
                print("         Expected:")
                print(expected_output)
                print("         Got:")
                print(actual_output)
                sys.exit(1)

            # handle exit codes
            shell.sendline("echo $?")
            shell.expect("echo [$][?]")
            shell.expect("\$ ")
            exitcode = int(shell.before.decode("utf-8").strip())
            if session.exitcodes and exitcode != session.exitcodes[i]:
                print("❌ Failed")
                print()
                print("         Expected exit code:", session.exitcodes[i])
                print("         Got exit code:", exitcode)
                sys.exit(1)

