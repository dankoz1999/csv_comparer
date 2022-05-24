from pathlib import Path
from typing import List

from domain.repositories import FileRepository


class Application:
    def __init__(self, file_repo: FileRepository, debug: bool = False) -> None:
        self.file_repo = file_repo
        self.debug = debug

    def basic_statistics(self, chosen_files: List[Path]) -> None:
        return None

    def full_statistics(file, chosen_files: List[Path]) -> None:
        return None
