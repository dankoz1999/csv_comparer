from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path
from typing import Dict, List

import pandas as pd

from comparer.templates import Config, DataFrameWithInfo


class ComparerFunction(ABC):
    def __init__(self, debug: bool, show_exceptions: bool, config: Config) -> None:
        self.debug = debug
        self.show_exceptions = show_exceptions
        self.config = config

    @abstractmethod
    def run(self, chosen_files: List[Path], output_dir: Path) -> int:
        pass

    def assign_table(
        self, chosen_files: List[Path], logger: Logger
    ) -> List[DataFrameWithInfo]:

        df_list: List[DataFrameWithInfo] = []
        self.counter: Dict[str, int] = {}
        for c in self.config.filename_type:
            self.counter[c] = 0
        for file in sorted(chosen_files):
            for i, file_t in enumerate(self.config.filename_type):
                if file_t in str(file):
                    df = pd.read_csv(str(file), sep=",", usecols=self.config.columns[i])
                    self.counter[file_t] = self.counter[file_t] + 1
                    index = self.config.filename_type.index(file_t)
                    exception_columns = (
                        self.config.exception_columns
                        if any(
                            [
                                elem in self.config.columns[i]
                                for elem in self.config.exception_columns
                            ]
                        )
                        else []
                    )
                    to_count = (
                        self.config.to_count
                        if any(
                            [
                                element[0] in self.config.columns[i]
                                for element in self.config.to_count
                            ]
                        )
                        else []
                    )
                    df_list.append(
                        DataFrameWithInfo(
                            df, exception_columns, to_count, file_t, file, index
                        )
                    )
        if self.debug:
            for key, value in self.counter.items():
                logger.info(f"Found {value} {key}")

        return df_list

    def assign_paths_visualization(
        self, chosen_files: List[Path]
    ) -> Dict[str, List[Path]]:
        dict_list: Dict[str, List[Path]] = {}
        for n in self.config.filename_type:
            dict_list[n] = []

        for path in chosen_files:
            for name in self.config.filename_type:
                if name in str(path):
                    dict_list[name].append(path)
                else:
                    raise ValueError("Csv file with invalid name!")

        return dict_list
