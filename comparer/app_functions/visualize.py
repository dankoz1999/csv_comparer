import difflib
import os
import platform
import webbrowser
from logging import Logger
from pathlib import Path
from typing import List

from comparer.app_functions import ComparerFunction
from comparer.templates import Config


class Visualize(ComparerFunction):
    def __init__(
        self, debug: bool, show_exceptions: bool, config: Config, logger: Logger
    ) -> None:
        super().__init__(debug, show_exceptions, config, logger)

    def run(self, chosen_files: List[Path], output_dir: Path) -> int:
        return self._visualize(chosen_files, output_dir)

    def _visualize(self, chosen_files: List[Path], output_dir: Path) -> int:
        files = self.assign_paths_visualization(chosen_files)
        # TODO add an ability to iterate thru every file
        fromfile = str(min(files["bottom_tables"], key=os.path.getctime))
        tofile = str(max(files["bottom_tables"], key=os.path.getctime))
        fromlines = open(fromfile, "U").readlines()
        tolines = open(tofile, "U").readlines()
        path = os.path.abspath(output_dir)
        path = os.path.join(path, "_diff.html")

        diff = difflib.HtmlDiff(wrapcolumn=70).make_file(
            fromlines, tolines, fromfile, tofile
        )

        with open(path, "w") as f:
            f.write(diff)
        if platform.system() == "Darwin":
            path = "file:///" + path
        webbrowser.get().open(path)
        return 0
