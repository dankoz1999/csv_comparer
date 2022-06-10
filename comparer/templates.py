from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


class FileRepository:
    def __init__(
        self,
        chosen_files: List[Path],
        output_dir: Path,
        skip_hidden: bool = True,
        debug: bool = False,
    ) -> None:
        self.output_dir = output_dir
        self.chosen_files = chosen_files
        self.skip_hidden = skip_hidden
        self.debug = debug

    @abstractmethod
    def get_files(self) -> List[Path]:
        pass


@dataclass
class DataFrameWithInfo:
    df: pd.DataFrame
    type: str
    filename: Path


@dataclass
class ListOfPaths:
    bottom_table: List[Path]
    equipment_table: List[Path]
    sensor_table: List[Path]
