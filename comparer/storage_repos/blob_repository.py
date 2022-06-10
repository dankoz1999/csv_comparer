from pathlib import Path
from typing import List, Set

from comparer.templates import FileRepository
from comparer.utils import find_file


# TODO add blob repository from scraper
class BlobRepository(FileRepository):
    def __init__(
        self,
        chosen_files: List[Path],
        skip_hidden: bool = True,
        debug: bool = False,
    ) -> None:
        self.chosen_files = chosen_files
        self.skip_hidden = skip_hidden
        self.debug = debug

    def get_files(self) -> List[Path]:
        res: Set[Path] = set()
        for chosen in self.chosen_files:
            files = find_file(chosen, "*csv", self.skip_hidden)
            if self.debug:
                print(f"Found {len(files)} {chosen} files")
            res.update(files)
        return [r for r in res]
