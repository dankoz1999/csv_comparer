
from logging import Logger
import os
from pathlib import Path
from typing import List
from dataclasses import fields
from csv_diff import compare, load_csv
import pandas as pd
from comparer.app_functions import ComparerFunction


class ShowDifference(ComparerFunction):
    def __init__(self, debug: bool, show_exceptions: bool) -> None:
        super().__init__(debug, show_exceptions)

    def run(self, chosen_files: List[Path],logger: Logger, output_dir:Path) -> None:
        return self._show_difference(chosen_files, logger, output_dir)

    def _show_difference(self, chosen_files: List[Path], logger: Logger,output_dir:Path) -> None:

        files = self._assign_paths_visualization(chosen_files)
        for field in fields(files):
            # print(field.name)
            type_ = getattr(files,field.name)
            if len(type_) > 1:
                comp_pre = min(type_, key= os.path.getctime)
                comp = max(type_, key=os.path.getctime)
                diff = compare(load_csv(open(comp_pre)), load_csv(open(comp)))
                logger.info(f"Saving {field.name}")
                for key, value in diff.items():
                    if key in ["added", "removed", "changed"]:
                        path = Path(str(output_dir) + "/" + f"{field.name}-{key}.csv")
                        if len(value) > 0:
                            for i, row in enumerate(value):
                                if i == 0:
                                    fin = pd.DataFrame([row])
                                else:
                                    fin = fin.append(row, ignore_index=True)
                        else:
                            logger.info(f"{key.capitalize()} table is empty, thus it won't be saved")
                            continue
                        logger.info(f"<--- Saving {key}.csv")
                        fin.to_csv(path)
            elif len(type_) ==1:
                logger.info("Cannot compare less than 2 files")
            else:
                pass