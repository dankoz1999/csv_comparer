import os
import platform
from typing import List
from pathlib import Path
import difflib
import webbrowser
from comparer.app_functions import ComparerFunction


class Visualize(ComparerFunction):
    def __init__(self, debug: bool, show_exceptions: bool) -> None:
        super().__init__(debug, show_exceptions)

    def run(self, chosen_files: List[Path], output_dir: Path) -> None:
        return self._visualize(chosen_files, output_dir)

    def _visualize(self, chosen_files: List[Path], output_dir: Path) -> None:
        files = self._assign_paths_visualization(chosen_files)
        fromfile = min(files.bottom_table, key=os.path.getctime)
        tofile = max(files.bottom_table, key=os.path.getctime)
        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()
        path = os.path.abspath(output_dir)
        path = os.path.join(path, "_diff.html")

        diff = difflib.HtmlDiff(wrapcolumn=70).make_file(fromlines,tolines,fromfile,tofile)

        with open(path, "w") as f:
            f.write(diff)
        if platform.system() == "Darwin":
            path = "file:///" + path
        # #TODO call Konrad and solve WSL issue
        # test = in_wsl()
        # run_html()
        webbrowser.get().open(path)