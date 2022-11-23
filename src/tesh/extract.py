""""""

from dataclasses import dataclass, field
import platform
import re

@dataclass
class ShellSession:
    code: str
    id: str
    ps1: str | None = None
    setup: str | None = None
    exitcodes: list[int] | None = None

def extract(f, max_num_lines: int = 100000) -> list[ShellSession]:
    sessions = dict()

    while True:
        line = f.readline()
        if not line:
            break

        lsline = line.lstrip()
        if lsline.startswith("```"):
            # normally ```, but can be more:
            num_leading_backticks = len(lsline) - len(lsline.lstrip("`"))

            # default
            num_leading_spaces = 0
            k = 1

            # get all directives that start with tesh- and remove the prefix
            directives = re.findall(r'tesh-(\w+)="([^"]+)"', lsline)

            # convert directives to a dict
            directives = dict(directives)

            # read the block
            code_block = []
            while True:
                line = f.readline()
                lsline = line.lstrip()

                # validation
                if not line:
                    raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )

                # check if end of block
                if lsline[:num_leading_backticks] == "`" * num_leading_backticks:
                    break

                if line == 1:
                  num_leading_spaces = len(line) - len(lsline)

                # remove leading spaces
                code_block.append(line[num_leading_spaces:])
                k += 1

            current_platform = platform.system().lower()
            if "session" in directives and directives.get("platform", current_platform) == current_platform:
                id_ = directives['session']
                if id_ in sessions:
                    session = sessions[id_]
                    session.code += "\n" + "\n".join(code_block)

                    ps1 = directives.get('ps1', None)
                    if ps1 and session.ps1:
                        raise RuntimeError("Multiple ps1 directives for same session aren't currently possible.")
                    elif ps1:
                        session.ps1 = ps1

                    exitcodes = parse_exitcodes(directives.get('exitcodes', ""))
                    if exitcodes and session.exitcodes:
                        session.exitcodes += exitcodes
                    if exitcodes and not session.exitcodes:
                        raise RuntimeError("If you're using exit codes for a session, you must specify them for all sessions.")

                    setup = directives.get('setup', None)
                    if setup:
                        # TODO: should we also check if setup would be overriden?
                        session.setup = setup

                else:
                    sessions[directives['session']] = ShellSession(
                        code="\n".join(code_block),
                        id = directives['session'],
                        ps1 = directives.get('ps1', None),
                        exitcodes = parse_exitcodes(directives.get('exitcodes', "")),
                        setup = directives.get('setup', None),
                    )

    return list(sessions.values())

def parse_exitcodes(exitcodes: str) -> list[int]:
    exitcodes = exitcodes.split()
    exitcodes = [int(exitcode) for exitcode in exitcodes]
    return exitcodes
