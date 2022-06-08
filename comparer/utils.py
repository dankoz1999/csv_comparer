import collections
from platform import uname
from pathlib import Path
from typing import Any, Callable, Iterable, List, TypeVar

T = TypeVar("T")


def find_file(root: Path, name: str, skip_hidden: bool = True) -> List[Path]:

    res: List[Path] = []
    for path in root.rglob(name):
        res.append(path.resolve())
    res = [r for r in res if r.is_file()]
    res = sorted(unique(res, key=lambda x: str(x).lower()))
    if skip_hidden:
        res = [p for p in res if not p.stem.startswith(".")]
    return res


def unique(l: Iterable[T], key: Callable[[T], Any]) -> List[T]:
    seen = collections.OrderedDict()
    for obj in l:
        # eliminate this check if you want the last item
        if key(obj) not in seen:
            seen[key(obj)] = obj
    return list(seen.values())

def in_wsl() -> bool:
    print(uname().release)
    return "microsoft-standard" in uname().release
