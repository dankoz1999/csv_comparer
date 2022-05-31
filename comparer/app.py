from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from comparer import get_logger
from comparer.templates import DataFrameWithInfo, FileRepository


class Application:
    def __init__(self, file_repo: FileRepository, debug: bool = False) -> None:
        self.file_repo = file_repo
        self.debug = debug
        self.logger = get_logger()

    def basic_statistics(self, chosen_files: List[Path]) -> None:
        df_list = self._assign_table(chosen_files)
        return self._summarize_basic(df_list, self.debug)

    def full_statistics(self, chosen_files: List[Path]) -> None:
        return None

    def visualize(self, chosen_files: List[Path]) -> None:
        return None

    def _summarize_basic(self, df_list: List[DataFrameWithInfo], debug: bool) -> None:
        first_bt = True
        first_eq = True
        first_sns = True
        for i, data in enumerate(df_list):
            df = data.df
            # Bottom Table
            if data.type == "bottom":
                if first_bt:
                    self.logger.info(" ")
                    self.logger.info(
                        "-------------Bottom Table Statistics-------------"
                    )
                    self.logger.info(" ")
                    first_bt = False
                if self.bt_count > 1:
                    self.logger.info(
                        f"Statistics for file nr {i+1} - {str(data.filename.stem)}"
                    )
                number_fill = 0
                for column, column1 in zip(
                    df["major_equipment"].notna(), df["major_equipment_parsed"].isna()
                ):
                    if column and column1:
                        number_fill += 1
                self.logger.info(
                    f"Found {number_fill} cells where Major Equipment is filled and Major Equipment Parse isn't"
                )
                number_dex = df.loc[
                    df["drawing_description"] == "Exception", "drawing_description"
                ].count()
                number_nex = df.loc[
                    df["drawing_number"] == "Exception", "drawing_number"
                ].count()
                number_tit = df.loc[
                    df["drawing_title_name"] == "Exception", "drawing_title_name"
                ].count()
                self.logger.info(
                    (f"Found {number_dex} exceptions in Drawing Description")
                )
                self.logger.info((f"Found {number_nex} exceptions in Drawing Number"))
                self.logger.info(
                    (f"Found {number_tit} exceptions in Drawing Title Name")
                )
                self.logger.info(" ")
            elif data.type == "equipment":
                if first_eq:
                    self.logger.info(" ")
                    self.logger.info("-------------Equipment Statistics-------------")
                    self.logger.info(" ")
                    first_eq = False
                if self.eq_count > 1:
                    self.logger.info(
                        f"Statistics for file nr {i+1 - self.bt_count} - {str(data.filename.stem)}"
                    )
                self.logger.info(f"Found {df.shape[0]} equipments")
                for item in ["primary-full", "primary-partial", "flow-table", "other"]:
                    value = df.loc[
                        df["scraped_equipment_type"] == item, "scraped_equipment_type"
                    ].count()
                    self.logger.info(f"Found {value} {item} equipment")
                to_long_desc = df.loc[
                    df["service_description"].str.len() > 50, "service_description"
                ].count()
                to_short_desc = df.loc[
                    df["service_description"].str.len() < 3, "service_description"
                ].count()
                self.logger.info(
                    f"Found {to_long_desc} equipment with description longer than 50"
                )
                self.logger.info(
                    f"Found {to_short_desc} equipment with description shorther than 3"
                )
                self.logger.info(" ")
            elif data.type == "sensor":
                if first_sns:
                    self.logger.info(" ")
                    self.logger.info("-------------Sensors Statistics-------------")
                    self.logger.info(" ")
                    first_sns = False
                if self.sns_count > 1:
                    self.logger.info(
                        f"Statistics for file nr {i+1 - self.bt_count - self.eq_count} - {str(data.filename.stem)}"
                    )
                df_number = self._sensors_preprocessing(df, debug)
                len_fil = len(df["filename"].unique())
                sns_number = df.shape[0] / df_number
                self.logger.info(f"Found {sns_number} sensors")
                self.logger.info(
                    f"Average number of sensors per diagram: {sns_number/len_fil} "
                )
                to_long_sns = df.loc[
                    df["sensor_name"].str.len() > 15, "sensor_name"
                ].count()
                to_short_sns = df.loc[
                    df["sensor_name"].str.len() < 3, "sensor_name"
                ].count()
                to_many_letters = df.loc[
                    df["sensor_name"].str.count("[A-Z]") > 9, "sensor_name"
                ].count()
                self.logger.info(
                    f"Found {to_long_sns} sensors with name longer than 15"
                )
                self.logger.info(
                    f"Found {to_short_sns} sensors with name shorter than 3"
                )
                self.logger.info(
                    f"Found {to_many_letters} sensors with more than 9 letters"
                )
                self.logger.info(" ")
        return None

    def _assign_table(self, chosen_files: List[Path]) -> List[DataFrameWithInfo]:

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
                fields = ["sensor_name", "primary_equipment_count", "filename"]
                df = pd.read_csv(str(file), sep=",", usecols=fields)
                self.sns_count += 1
                df_list.append(DataFrameWithInfo(df, "sensor", file))
            else:
                raise ValueError("Csv file with invalid name!")
        if self.debug:
            self.logger.info(
                f"Found {self.bt_count} Bottom Tables, {self.eq_count} Equipment Tables and {self.sns_count} Sensor Tables"
            )
        return df_list

    def _sensors_preprocessing(self, df: pd.DataFrame, debug: bool) -> int:

        filenames = df["filename"].unique()
        occurances = df["filename"].value_counts()
        value_counts = df.groupby("filename")["primary_equipment_count"].max()
        value_counts = value_counts[np.logical_not(np.isnan(value_counts))]
        counter = 0
        bad_diagrams: List[str] = []
        for f in filenames:
            f_occurances = occurances[f]
            try:
                value_count = value_counts[f]
            except:
                value_count = 1
            counter = f_occurances / value_count
            if counter != int(counter):
                if debug:
                    self.logger.debug(f"There are not found eq in {f}")
                bad_diagrams.append(f)
        if len(bad_diagrams) > 0:
            self.logger.info(f"There is not found eq in {len(bad_diagrams)} diagrams")
            self.logger.info("Fix them, if you want to have exact number of sensors!")
            self.logger.info(" ")
            self.logger.info("List of bad diagrams: ")
            for diagram in bad_diagrams:
                self.logger.info(f"--> {diagram}")
            self.logger.info(" ")
        return counter
