from logging import Logger
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from comparer.app_functions import ComparerFunction
from comparer.templates import Config, DataFrameWithInfo


class BasicStatistics(ComparerFunction):
    def __init__(
        self, debug: bool, show_exceptions: bool, config: Config, logger: Logger
    ) -> None:
        super().__init__(debug, show_exceptions, config, logger)

    def run(self, chosen_files: List[Path], output_dir: Path) -> int:
        df_list = self.assign_table(chosen_files, self.logger)
        if len(df_list) == 0:
            self.logger.warning("No tables assigned!")
            return 0
        return self._summarize_basic(df_list, self.debug)

    def _summarize_basic(self, df_list: List[DataFrameWithInfo], debug: bool) -> int:
        bool_values: Dict[str, bool] = {}
        for key in self.counter.keys():
            bool_values[key] = True
        if not self.show_exceptions:
            self.logger.info(
                "To get more informations columns with exceptions use --show-exceptions"
            )
            self.logger.info(" ")
        for i, data in enumerate(df_list):
            df = data.df
            if len(self.config.aliases) > 0:
                data.type = self.config.aliases[data.index]
            if bool_values[data.type]:
                self.logger.info(" ")
                self.logger.info(
                    f"-------------{data.type.capitalize()} Statistics-------------"
                )
                self.logger.info(" ")
                bool_values[data.type] = False
            if self.counter[data.type] > 1:
                self.logger.info(
                    f"Statistics for file nr {i+1} - {str(data.filename.stem)}"
                )
            # BT
            if (
                data.type == self.config.filename_type[0]
                or data.type == self.config.filename_type[1]
            ):
                self.logger.info(f"Found {df.shape[0]} {data.type}")
                for exception in data.exception_columns:
                    number = df.loc[
                        df[exception] == self.config.exception_style, exception
                    ].count()
                    self.logger.info(f"Found {number} exceptions in {exception}")
                for ct in data.to_count:
                    if ct[1] == "gt":
                        counted_value = df.loc[
                            df[ct[0]].str.len() > int(ct[2]), ct[0]
                        ].count()
                        self.logger.info(
                            f"Found {counted_value} {data.type} with {ct[0]} longer than {ct[2]}"
                        )
                    elif ct[1] == "lt":
                        counted_value = df.loc[
                            df[ct[0]].str.len() < int(ct[2]), ct[0]
                        ].count()
                        self.logger.info(
                            f"Found {counted_value} {data.type} with {ct[0]} shorther than {ct[2]}"
                        )
                    else:
                        raise ValueError(
                            "Invalid comparison sign -> use gt for > or lt for <"
                        )
                self.logger.info(" ")
            # EQ
            elif data.type == self.config.filename_type[1]:
                for item in sorted(df[self.config.columns[data.index][3]].unique()):
                    value = df.loc[
                        df[self.config.columns[data.index][3]] == item,
                        self.config.columns[data.index][3],
                    ].count()
                    self.logger.info(f"Found {value} {item} {data.type}")
            # S
            elif data.type == self.config.filename_type[2]:
                df_number = self._preprocessing(df, debug, data)
                len_fil = len(df[self.config.columns[2][2]].unique())
                number = df.shape[0] / df_number
                self.logger.info(f"Found {int(number)} {data.type}")
                self.logger.info(
                    f"Average number of {data.type} per file: {int(number/len_fil)} "
                )
                to_long = df.loc[
                    df[self.config.columns[data.index][0]].str.len() > 15,
                    self.config.columns[data.index][0],
                ].count()
                to_short = df.loc[
                    df[self.config.columns[data.index][0]].str.len() < 3,
                    self.config.columns[data.index][0],
                ].count()
                to_many_letters = df.loc[
                    df[self.config.columns[data.index][0]].str.count("[A-Z]") > 9,
                    self.config.columns[data.index][0],
                ].count()
                self.logger.info(
                    f"Found {to_long} {data.type} with name longer than 15"
                )
                self.logger.info(
                    f"Found {to_short} {data.type} with name shorter than 3"
                )
                self.logger.info(
                    f"Found {to_many_letters} {data.type} with more than 9 letters"
                )
                self.logger.info(" ")
        return 0

    def _preprocessing(
        self, df: pd.DataFrame, debug: bool, data: DataFrameWithInfo
    ) -> int:

        filenames = df[self.config.columns[data.index][2]].unique()
        occurances = df[self.config.columns[data.index][2]].value_counts()
        value_counts = df.groupby(self.config.columns[data.index][2])[
            self.config.columns[data.index][1]
        ].max()
        value_counts = value_counts[np.logical_not(np.isnan(value_counts))]
        counter = 0
        bad_files: List[str] = []
        for f in filenames:
            f_occurances = occurances[f]
            try:
                value_count = value_counts[f]
            except:
                value_count = 1
            counter = f_occurances / value_count
            if counter != int(counter):
                if debug:
                    self.logger.debug(f"There is a problem in {f}")
                bad_files.append(f)
        if len(bad_files) > 0:
            self.logger.info(f"There is a problem in {len(bad_files)} files")
            self.logger.info(
                f"Fix them, if you want to have exact number of {data.type}!"
            )
            if self.show_exceptions:
                self.logger.info(" ")
                self.logger.info("List of bad files: ")
                for file in bad_files:
                    self.logger.info(f"--> {file}")
                self.logger.info(" ")
        return counter
