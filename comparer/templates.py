from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


class FileRepository:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_files(self) -> List[Path]:
        pass


@dataclass
class DataFrameWithInfo:
    df: pd.DataFrame
    type: str
    filename: Path
