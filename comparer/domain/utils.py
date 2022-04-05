from pathlib import Path
from typing import List


def find_file(root: Path, name: str, skip_hidden: bool = True) -> List[Path]:

    res = List[Path] = []

    for path in root.rglob(name):
        res.append(path)
    res = [r for r in res if is_csv(r)]

    return res


def is_csv(path: Path, name: str = ".csv") -> bool:
    return True if path in path.rglob(name) else False
