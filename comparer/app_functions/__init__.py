from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path
from typing import List

import pandas as pd

from comparer.templates import DataFrameWithInfo, ListOfPaths


class ComparerFunction(ABC):
    def __init__(self, debug: bool, show_exceptions: bool) -> None:
        self.debug = debug
        self.show_exceptions = show_exceptions

    @abstractmethod
    def run(self, chosen_files: List[Path], output_dir: Path) -> int:
        pass

    def assign_table(
        self, chosen_files: List[Path], logger: Logger
    ) -> List[DataFrameWithInfo]:

        df_list: List[DataFrameWithInfo] = []
        self.bt_count = 0
        self.eq_count = 0
        self.sns_count = 0
        for file in sorted(chosen_files):
            if "bottom_tables" in str(file):
                fields = [
                    "filename",
                    "drawing_number",
                    "drawing_title_name",
                    "drawing_description",
                    "major_equipment",
                    "major_equipment_parsed",
                ]
                df = pd.read_csv(str(file), sep=",", usecols=fields)
                self.bt_count += 1
                df_list.append(DataFrameWithInfo(df, "bottom", file))
            elif "equipment" in str(file):
                fields = [
                    "service_description",
                    "yard_no",
                    "equipment_code",
                    "scraped_equipment_type",
                ]
                df = pd.read_csv(str(file), sep=",", usecols=fields)
                self.eq_count += 1
                df_list.append(DataFrameWithInfo(df, "equipment", file))
            elif "tag_assignments" in str(file):
                fields = [
                    "sensor_name",
                    "primary_equipment_count",
                    "filename",
                    "equipment_code",
                ]
                df = pd.read_csv(str(file), sep=",", usecols=fields)
                self.sns_count += 1
                df_list.append(DataFrameWithInfo(df, "sensor", file))
            else:
                raise ValueError("Csv file with invalid name!")
        if self.debug:
            logger.info(
                f"Found {self.bt_count} Bottom Tables, {self.eq_count} Equipment Tables and {self.sns_count} Sensor Tables"
            )
        return df_list

    def assign_paths_visualization(self, chosen_files: List[Path]) -> ListOfPaths:
        bt_list: List[Path] = []
        eq_list: List[Path] = []
        sns_list: List[Path] = []

        for path in chosen_files:
            if "bottom_tables" in str(path):
                bt_list.append(path)
            elif "equipment" in str(path):
                eq_list.append(path)
            elif "tag_assignment" in str(path):
                sns_list.append(path)
            else:
                raise ValueError("Csv file with invalid name!")

        return ListOfPaths(bt_list, eq_list, sns_list)
