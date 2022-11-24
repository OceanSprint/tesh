"""Initialize the tesh runner."""

from pathlib import Path
from tesh.extract import extract
from tesh.extract import extract_blocks
from tesh.test import test

import click
import typing as t


@click.command()
@click.argument("paths", nargs=-1)
@click.option("--ext", default="md", help="Extension of files to extract from.")
@click.option("--verbose", is_flag=True, default=False)
@click.version_option()
def run(paths: t.Set[str], ext: str, verbose: bool) -> None:
    """Collect and test code blocks."""

    filenames = []

    # collect all markdown files
    for path in paths:
        if path.endswith(ext):
            filenames.append(path)
        else:
            for subpath in Path(path).rglob("*." + ext):
                filenames.append(str(subpath))

    # remove duplicates
    filenames = list(set(filenames))
    filenames.sort()

    for filename in filenames:
        print("📄 Checking", filename)  # noqa: ENC100
        with open(filename) as f:
            sessions = extract(f)

        for session in sessions:
            print("  ✨ Running", session.id_, " ", end="") # noqa: ENC100
            extract_blocks(session, verbose)
            test(filename, session, verbose)
            print("✅ Passed") # noqa: ENC100
