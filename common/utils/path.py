import shutil

from pathlib import Path


def create_path(path: str, overwrite: bool = False) -> None:
    if overwrite:
        shutil.rmtree(path, ignore_errors=True)

    Path(path).mkdir(parents=True, exist_ok=True)
