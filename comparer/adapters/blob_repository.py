from pathlib import Path
from typing import List, Set

from comparer.domain.repositories import FileRepository
from comparer.domain.utils import find_file


# TODO add blob repository from scraper
class BlobRepository(FileRepository):
    def __init__(
        self,
        data_dir: Path,
        chosen_files: List[str],
        skip_hidden: bool = True,
        debug: bool = False,
    ) -> None:
        self.data_dir = data_dir
        self.chosen_files = chosen_files
        self.skip_hidden = skip_hidden
        self.debug = debug

    def get_files(self) -> List[Path]:
        res: Set[Path] = set()
        for chosen in self.chosen_files:
            files = find_file(self.data_dir, chosen, self.skip_hidden)
            if self.debug:
                print(f"Found {len(files)} {chosen} files")
            res.update(files)
        return [r for r in res]
