import os
from logging import Logger
from pathlib import Path
from typing import List

import pandas as pd
from csv_diff import compare, load_csv

from comparer.app_functions import ComparerFunction
from comparer.templates import Config


class ShowDifference(ComparerFunction):
    def __init__(
        self, debug: bool, show_exceptions: bool, config: Config, logger: Logger
    ) -> None:
        super().__init__(debug, show_exceptions, config, logger)

    def run(self, chosen_files: List[Path], output_dir: Path) -> int:
        return self._show_difference(chosen_files, output_dir)

    def _show_difference(self, chosen_files: List[Path], output_dir: Path) -> int:

        files = self.assign_paths_visualization(chosen_files)
        for field_key, field in files.items():
            if len(field) > 1:
                comp_pre = min(field, key=os.path.getctime)
                comp = max(field, key=os.path.getctime)
                if self.config.show_difference_key is not None:
                    diff = compare(
                        load_csv(open(comp_pre), key=self.config.show_difference_key),
                        load_csv(open(comp), key=self.config.show_difference_key),
                    )
                else:
                    file_pre = pd.read_csv(str(comp_pre), on_bad_lines="skip")
                    key_pre = file_pre.columns.values[0]
                    diff = compare(
                        load_csv(open(comp_pre), key=key_pre),
                        load_csv(open(comp), key=key_pre),
                    )
                self.logger.info(f"Saving {field_key}")
                for key, value in diff.items():
                    if key in ["added", "removed", "changed"]:
                        path = Path(str(output_dir) + "/" + f"{field_key}-{key}.csv")
                        if len(value) > 0:
                            for i, row in enumerate(value):
                                if i == 0:
                                    fin = pd.DataFrame([row])
                                else:
                                    fin = fin.append(row, ignore_index=True)
                        else:
                            self.logger.info(
                                f"{key.capitalize()} table is empty, thus it won't be saved"
                            )
                            continue
                        self.logger.info(f"<--- Saving {key}.csv")
                        fin.to_csv(path)
            elif len(field) == 1:
                self.logger.info("Cannot compare less than 2 files")
            else:
                pass
        return 0
