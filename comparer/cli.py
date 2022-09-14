from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from comparer.app import Application
from comparer.service import new_application


class Cli:

    modes = {"basic_statistics", "show_difference", "visualize"}

    def __init__(self, app: Application, mode: str) -> None:
        self.app = app
        self.mode = mode
        self.mode_flow = {
            "basic_statistics": self.basic_stat_flow,
            "show_difference": self.show_difference_flow,
            "visualize": self.visualize_flow,
        }
        if not self.modes == set(self.mode_flow.keys()):
            raise ValueError("Incorrect modes!")

    @classmethod
    def new_cli_app(cls, args: List[str]) -> Cli:
        parsed_args = Cli.parse_args(*args)
        app = new_application(
            chosen_files=parsed_args.chosen_files,
            output_dir=Path(*parsed_args.output_dir),
            filename_type=parsed_args.filename_type,
            aliases=parsed_args.aliases,
            columns=parsed_args.columns,
            exception_style=parsed_args.exception_style,
            exception_columns=parsed_args.exception_columns,
            to_count=parsed_args.to_count,
            show_difference_key=parsed_args.show_diff_key,
            skip_hidden=parsed_args.skip_hidden,
            show_exceptions=parsed_args.show_exceptions,
            debug=parsed_args.debug,
        )
        mode = parsed_args.mode
        return cls(app, mode)

    def run(self) -> int:
        chosen_files = self.app.file_repo.get_files()
        run_fun = self.mode_flow.get(self.mode)
        if run_fun is None:
            raise ValueError(f"Mode {self.mode} not found")

        return run_fun(chosen_files)

    def basic_stat_flow(self, chosen_files: List[Path]) -> int:
        return self.app.basic_statistics(chosen_files)

    def show_difference_flow(self, chosen_files: List[Path]) -> int:
        return self.app.show_difference(chosen_files)

    def visualize_flow(self, chosen_files: List[Path]) -> int:
        return self.app.visualize(chosen_files)

    @staticmethod
    def parse_args(*args: str) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Csv comparer is an application to compare two or more csv files"
        )
        parser.add_argument(
            "--mode",
            choices=Cli.modes,
            help="chose wheter you want to obtain basic funcionality or show difference [basic_statistics, show_difference]",
            default="basic_statistics",
            required=True,
        )

        parser.add_argument(
            "--chosen-files",
            type=str,
            nargs="+",
            help="list of paths to files",
            default=[],
            required=True,
        )

        parser.add_argument(
            "--output-dir",
            type=str,
            nargs="+",
            help="directory to store results",
            default=[],
            required=True,
        )

        parser.add_argument(
            "--skip-hidden",
            help="comparing hidden files",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--debug",
            help="decide wheter you want more info",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--show-exceptions",
            help="show/hide files with exceptions or problems",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--filename-type",
            type=str,
            nargs="+",
            help="enter the names of filenames which should be compared (files need to have the same unique part)",
            required=True,
        )

        parser.add_argument(
            "--aliases",
            type=str,
            nargs="+",
            help="enter the aliases if you want to have different names than the files",
        )

        parser.add_argument(
            "--columns",
            type=str,
            nargs="+",
            help="specify column names for each set of files",
            action="append",
            default=[],
        )

        parser.add_argument(
            "--exception-style",
            type=str,
            help="enter custom exception style ('Exception' by default)",
            default="Exception",
        )

        parser.add_argument(
            "--exception-columns",
            type=str,
            nargs="+",
            help="specify column names for each set of files",
        )

        parser.add_argument(
            "--to-count",
            type=str,
            nargs="+",
            help="specify columns which are supposed to be counted and add max or min value (for example if you want to calculate col. 'abc' >/< 10 signs use abc gt/lt 10) ",
        )

        parser.add_argument(
            "--show-diff-key",
            type=str,
            help="specify unique key (column name). If not the first name will be set as the key",
            default=None,
        )

        namespace = parser.parse_args(args)

        file_paths: List[str] = list(namespace.chosen_files)
        for path in file_paths:
            if not (Path(path).is_file() or Path(path).is_dir()):
                raise ValueError(f"{path} doesn't exist!")

        return namespace
