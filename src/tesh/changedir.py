from contextlib import contextmanager
from pathlib import Path

import os
# Remove once we support Python 3.11+
@contextmanager
def changedir(path: Path):
    """Sets the cwd within the context

    Args:
        path (Path): The path to the cwd

    Yields:
        None
    """

    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)
