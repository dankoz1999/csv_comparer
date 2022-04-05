from abc import abstractmethod
from pathlib import Path
from typing import List


class FileRepository:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_files(self) -> List[Path]:
        pass
