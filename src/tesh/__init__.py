"""Initialize the tesh command."""

from pathlib import Path
from tesh.extract import extract, extract_blocks
from tesh.test import test

import click


@click.command()
@click.argument("paths", nargs=-1)
@click.option("--ext", default="md", help="Extension of files to extract from.")
@click.option("--verbose", is_flag=True, default=False)
def run(paths, ext, verbose):
    filenames = []

    # collect all markdown files
    for path in paths:
        if path.endswith(ext):
            filenames.append(path)
        else:
            for path in Path(path).rglob("*." + ext):
                filenames.append(path.name)

    for filename in filenames:
        print("📄 Checking", filename)
        with open(filename) as f:
            sessions = extract(f)

        for session in sessions:
            print("  ✨ Running", session.id)
            extract_blocks(session, verbose)
            test(filename, session, verbose)
