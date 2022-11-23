import pexpect
import os
from pathlib import Path

def test(filename, session, verbose: bool):
    with Path(filename).parent:
        shell = pexpect.spawn(session.setup or 'sh')
        for block in session.blocks:
            if verbose:
                print("      ", block)
            shell.sendline(block.command)

            if "DEBUG" in block.output:
                shell.interact()

            shell.expect("\n".join(block.output).replace("...", ".*"))

            # TODO: handle exit codes
