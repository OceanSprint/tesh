"""Initialize the tesh command."""

import click
from pathlib import Path

from .extract import extract


@click.command()
@click.argument('paths', nargs=-1)
@click.option('--ext', default="md", help='Extension of files to extract from.')
def run(paths, ext):
    filenames = []

    # collect all markdown files
    for path in paths:
        if path.endswith(ext):
            filenames.append(path)
        else:
            for path in Path(path).rglob('*.' + ext):
                filenames.append(path.name)

    for filename in filenames:
        print("📄 Checking", filename)
        with open(filename) as f:
            sessions = extract(f)

        for session in sessions:
            print("  ✨ Running", session.id)
            #print("   ", session)

            # TODO: turn sessions into a format for pexpect
            # TODO: run pexpect
>>>>>>> 6f528ec (extract)
