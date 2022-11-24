"""Temporary hack until Python 3.11+."""

from contextlib import contextmanager
from pathlib import Path

import os
import typing as t


# Remove once we support Python 3.11+
@contextmanager
def changedir(path: Path) -> t.Iterator[None]:
    """Set the cwd within the context."""

    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)
