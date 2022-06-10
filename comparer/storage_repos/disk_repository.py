from pathlib import Path
from typing import List, Set

from comparer import get_logger
from comparer.templates import FileRepository
from comparer.utils import find_file

logger = get_logger()


class DiskRepository(FileRepository):
    def __init__(
        self,
        chosen_files: List[Path],
        output_dir: Path,
        skip_hidden: bool = True,
        debug: bool = False,
    ) -> None:
        super().__init__(chosen_files, output_dir, skip_hidden, debug)

    def get_files(self) -> List[Path]:
        res: Set[Path] = set()
        for chosen in self.chosen_files:
            if chosen.is_dir():
                files = find_file(chosen, "*csv", self.skip_hidden)
                res.update(files)
            elif chosen.is_file():
                res.update([chosen])
            if self.debug:
                if len(res) > 1:
                    logger.debug(f"Found {len(res)} csv files")
                elif len(res) == 0:
                    logger.debug("Didn't find any files!")
                else:
                    logger.debug("Found 1 file")
        return [r for r in res]
