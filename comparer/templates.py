from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


class FileRepository(ABC):
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
    exception_columns: List[str]
    to_count: List[str]
    type: str
    filename: Path
    index: int


@dataclass
class ListOfPaths:
    bottom_table: List[Path]
    equipment_table: List[Path]
    sensor_table: List[Path]


@dataclass
class Config:
    filename_type: List[str]
    columns: List[List[str]]
    exception_style: str
    exception_columns: List[str]
    to_count: List[str]
    aliases: List[str]
    show_difference_key: str
