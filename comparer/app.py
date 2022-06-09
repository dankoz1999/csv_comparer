from pathlib import Path
from typing import List


from comparer import get_logger
from comparer.templates import FileRepository
from comparer.app_functions.basic_statistics import BasicStatistics
from comparer.app_functions.show_difference import ShowDifference
from comparer.app_functions.visualize import Visualize

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class Application:
    def __init__(
        self, file_repo: FileRepository, show_exceptions: bool, debug: bool = False
    ) -> None:
        self.file_repo = file_repo
        self.show_exceptions = show_exceptions
        self.debug = debug
        self.logger = get_logger()

    def basic_statistics(self, chosen_files: List[Path]) -> None:
        bs = BasicStatistics(self.debug, self.show_exceptions)
        return bs.run(chosen_files, self.logger)

    def show_difference(self, chosen_files: List[Path]) -> None:
        sd = ShowDifference(self.debug, self.show_exceptions)
        return sd.run(chosen_files, self.logger, self.file_repo.output_dir)

    def visualize(self, chosen_files: List[Path]) -> None:
        vi = Visualize(self.debug, self.show_exceptions)
        return vi.run(chosen_files, self.file_repo.output_dir)


