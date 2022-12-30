"""Initialize the tesh runner."""

from pathlib import Path
from tesh.changedir import changedir
from tesh.extract import extract
from tesh.extract import extract_blocks
from tesh.extract import fail
from tesh.test import test
from tesh.test import write_fixtures

import click
import os.path
import shutil
import sys
import tempfile
import typing as t


@click.command()
@click.argument("paths", nargs=-1)
@click.option("--ext", default="md", help="Extension of files to extract from.")
@click.option("--verbose", is_flag=True, default=False)
@click.option("--no-debug", "debug", flag_value=False)
@click.option("--debug", "debug", flag_value=True, default=sys.stdin.isatty())
@click.version_option()
def tesh(paths: t.Set[str], ext: str, verbose: bool, debug: bool) -> None:
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
            with tempfile.TemporaryDirectory() as tmpdirname:
                tmpdir = Path(tmpdirname)
                if session.setup:
                    setup = Path(filename).parent / session.setup
                    if not os.path.exists(setup):
                        fail("Setup file does not exist:", setup)
                    shutil.copyfile(setup, tmpdir / session.setup)
                with changedir(tmpdir):
                    print("  ✨ Running", session.id_, " ", end="", flush=True)  # noqa
                    extract_blocks(session, verbose)
                    write_fixtures(session)
                    test(filename, session, verbose, debug)
                    print("✅ Passed")  # noqa: ENC100
