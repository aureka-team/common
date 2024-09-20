import json

from itertools import groupby
from typing import Iterator, Iterable


def get_pretty(
    obj: dict | list[dict],
    indent: int = 4,
    ensure_ascii: bool = False,
) -> str:
    return json.dumps(
        obj,
        indent=indent,
        ensure_ascii=ensure_ascii,
    )


def save_json(
    obj: dict | list[dict],
    file_path: str,
    indent: int = 4,
) -> None:
    with open(file_path, "w") as f:
        f.write(get_pretty(obj=obj, indent=indent))


def load_json(json_file_path: str) -> dict | list[dict]:
    with open(json_file_path, "r") as f:
        content = json.loads(f.read())
        return content


def get_unique(dict_list: list[dict]) -> Iterator[dict]:
    unique = set(map(json.dumps, dict_list))
    return map(json.loads, unique)


def group_by_key(
    dict_iter: Iterable[dict],
    group_key: str,
    sort_key: str | None = None,
) -> Iterator[list[dict]]:
    if sort_key is not None:
        dict_iter = sorted(dict_iter, key=lambda x: x[sort_key])

    return (list(g[1]) for g in groupby(dict_iter, lambda x: x[group_key]))
