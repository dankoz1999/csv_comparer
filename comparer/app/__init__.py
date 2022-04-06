from pathlib import Path
from typing import List

from domain.repositories import FileRepository


class Application:
    def __init__(self, file_repo: FileRepository, debug: bool = False) -> None:
        self.file_repo = file_repo
        self.debug = debug

    def basic_statistics(filepath: Path, chosen_files: List[str]) -> None:
        pass
