

from logging import Logger
from pathlib import Path
from typing import List
from comparer.app_functions import ComparerFunction
from comparer.templates import DataFrameWithInfo
import pandas as pd
import numpy as np


class BasicStatistics(ComparerFunction):
    def __init__(self, debug: bool, show_exceptions: bool) -> None:
        super().__init__(debug, show_exceptions)

    def run(self, chosen_files: List[Path], logger: Logger) -> None:
        df_list = self._assign_table(chosen_files, logger)
        return self._summarize_basic(df_list, self.debug,logger)

    def _summarize_basic(self, df_list: List[DataFrameWithInfo], debug: bool, logger: Logger) -> None:
        first_bt = True
        first_eq = True
        first_sns = True
        if not self.show_exceptions:
            logger.info(
                "To get information about names of diagrams with exceptions/not_found_eq use --show-exceptions"
            )
            logger.info(" ")
        for i, data in enumerate(df_list):
            df = data.df
            # Bottom Table
            if data.type == "bottom":
                if first_bt:
                    logger.info(" ")
                    logger.info(
                        "-------------Bottom Table Statistics-------------"
                    )
                    logger.info(" ")
                    first_bt = False
                if self.bt_count > 1:
                    logger.info(
                        f"Statistics for file nr {i+1} - {str(data.filename.stem)}"
                    )
                number_fill = 0
                for column, column1 in zip(
                    df["major_equipment"].notna(), df["major_equipment_parsed"].isna()
                ):
                    if column and column1:
                        number_fill += 1
                logger.info(
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
                logger.info(
                    (f"Found {number_dex} exceptions in Drawing Description")
                )
                logger.info((f"Found {number_nex} exceptions in Drawing Number"))
                logger.info(
                    (f"Found {number_tit} exceptions in Drawing Title Name")
                )
                logger.info(" ")
            elif data.type == "equipment":
                if first_eq:
                    logger.info(" ")
                    logger.info("-------------Equipment Statistics-------------")
                    logger.info(" ")
                    first_eq = False
                if self.eq_count > 1:
                    logger.info(
                        f"Statistics for file nr {i+1 - self.bt_count} - {str(data.filename.stem)}"
                    )
                logger.info(f"Found {df.shape[0]} equipments")
                for item in ["primary-full", "primary-partial", "flow-table", "other"]:
                    value = df.loc[
                        df["scraped_equipment_type"] == item, "scraped_equipment_type"
                    ].count()
                    logger.info(f"Found {value} {item} equipment")
                to_long_desc = df.loc[
                    df["service_description"].str.len() > 50, "service_description"
                ].count()
                to_short_desc = df.loc[
                    df["service_description"].str.len() < 3, "service_description"
                ].count()
                logger.info(
                    f"Found {to_long_desc} equipment with description longer than 50"
                )
                logger.info(
                    f"Found {to_short_desc} equipment with description shorther than 3"
                )
                logger.info(" ")
            elif data.type == "sensor":
                if first_sns:
                    logger.info(" ")
                    logger.info("-------------Sensors Statistics-------------")
                    logger.info(" ")
                    first_sns = False
                if self.sns_count > 1:
                    logger.info(
                        f"Statistics for file nr {i+1 - self.bt_count - self.eq_count} - {str(data.filename.stem)}"
                    )
                df_number = self._sensors_preprocessing(df, debug, logger)
                len_fil = len(df["filename"].unique())
                sns_number = df.shape[0] / df_number
                logger.info(f"Found {int(sns_number)} sensors")
                logger.info(
                    f"Average number of sensors per diagram: {int(sns_number/len_fil)} "
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
                logger.info(
                    f"Found {to_long_sns} sensors with name longer than 15"
                )
                logger.info(
                    f"Found {to_short_sns} sensors with name shorter than 3"
                )
                logger.info(
                    f"Found {to_many_letters} sensors with more than 9 letters"
                )
                logger.info(" ")

    def _sensors_preprocessing(self, df: pd.DataFrame, debug: bool, logger: Logger) -> int:

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
                    logger.debug(f"There are not found eq in {f}")
                bad_diagrams.append(f)
        if len(bad_diagrams) > 0:
            logger.info(f"There is not found eq in {len(bad_diagrams)} diagrams")
            logger.info("Fix them, if you want to have exact number of sensors!")
            if self.show_exceptions:
                logger.info(" ")
                logger.info("List of bad diagrams: ")
                for diagram in bad_diagrams:
                    logger.info(f"--> {diagram}")
                logger.info(" ")
        return counter