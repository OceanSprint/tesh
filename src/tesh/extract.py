"""Extract testable sessions from Markdown files."""

from dataclasses import dataclass
from dataclasses import field

import platform
import re
import sys
import typing as t


@dataclass
class Fixture:
    """Files for a session."""

    filename: str
    contents: str


@dataclass
class Block:
    """Shell sessions are constructed of blocks.

    Each block has a line of command followed by one or more lines of output.
    """

    command: t.Optional[str] = None
    output: t.List[str] = field(default_factory=lambda: [])


@dataclass
class ShellSession:
    """A code block showing a shell session in Markdown."""

    lines: list[str]
    blocks: list[Block]
    id_: str
    ps1: t.Union[str, None] = None
    setup: t.Union[str, None] = None
    exitcodes: list[int] = field(default_factory=lambda: [])
    fixtures: list[Fixture] = field(default_factory=lambda: [])


def extract(
    f: t.TextIO, max_num_lines: int = 100000
) -> list[ShellSession]:  # pragma: no cover  # TODO
    """Extract testable shell sessions from a Markdown file."""
    sessions: dict["str", ShellSession] = {}

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
            directives = dict(re.findall(r'tesh-(\w+)="([^"]+)"', lsline))

            # read the block
            code_lines = []
            while True:
                line = f.readline()
                lsline = line.lstrip()

                # validation
                if not line:
                    raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(f"File too large (> {max_num_lines} lines).")

                # check if end of block
                if lsline[:num_leading_backticks] == "`" * num_leading_backticks:
                    break

                if k == 1:
                    num_leading_spaces = len(line) - len(lsline)

                # remove leading spaces
                code_lines.append(line[num_leading_spaces:])
                k += 1

            current_platform = platform.system().lower()
            if (
                "session" in directives
                and directives.get("platform", current_platform) == current_platform
            ):
                id_ = directives["session"]
                if fixture := directives.get("fixture"):
                    if id_ in sessions:
                        session = sessions[id_]
                    else:
                        session = ShellSession(id_=id_, lines=[], blocks=[])
                        sessions[id_] = session

                    session.fixtures.append(Fixture(fixture, "\n".join(code_lines)))
                    continue

                if id_ in sessions:
                    session = sessions[id_]
                    session.lines += code_lines

                    ps1 = directives.get("ps1", None)
                    if ps1 and session.ps1:
                        fail(
                            "Multiple ps1 directives for same session aren't currently possible."
                        )
                    elif ps1:
                        session.ps1 = ps1

                    exitcodes = parse_exitcodes(directives.get("exitcodes", ""))
                    if exitcodes:
                        session.exitcodes += exitcodes

                    setup = directives.get("setup", None)
                    if setup:
                        # TODO: should we also check if setup would be overridden?
                        session.setup = setup

                else:
                    sessions[id_] = ShellSession(
                        lines=code_lines,
                        blocks=[],
                        id_=directives["session"],
                        ps1=directives.get("ps1", None),
                        exitcodes=parse_exitcodes(directives.get("exitcodes", "")),
                        setup=directives.get("setup", None),
                    )

    return list(sessions.values())


def fail(*msg):
    print("❌ Failed")
    print("    ", *msg)
    sys.exit(1)


def extract_blocks(session: ShellSession, verbose: bool) -> None:
    """Extract blocks from sessions."""
    prompt = re.compile(r"^(\$|{ps1}) ".format(ps1=session.ps1))
    new_block = Block()
    blocks = []

    for line in session.lines:
        if prompt.match(line):
            if new_block.command:
                blocks.append(new_block)
            new_block = Block()
            new_block.command = re.sub(prompt, "", line).strip()
        elif not line.strip():
            continue
        else:
            new_block.output.append(line.strip())
    blocks.append(new_block)
    session.blocks = blocks

    if session.exitcodes and (len(session.exitcodes) != len(session.blocks)):
        fail(
            "If you're using exit codes for a session, you must specify them for all commands."
        )


def parse_exitcodes(exitcodes_spec: str) -> list[int]:
    """Parse '0 1 0' spec of exitcodes into a list of ints."""
    return [int(exitcode) for exitcode in exitcodes_spec.split()]
