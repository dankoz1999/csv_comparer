from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from comparer.app import Application
from comparer.service import new_application


class Cli:

    modes = {"basic_statistics", "full_statistics", "visualize"}

    def __init__(self, app: Application, mode: str) -> None:
        self.app = app
        self.mode = mode
        self.mode_flow = {
            "basic_statistics": self.basic_stat_flow,
            "full_statistics": self.full_statistics_flow,
            "visualize": self.visualize_flow,
        }
        if not self.modes == set(self.mode_flow.keys()):
            raise ValueError("Incorrect modes!")

    @classmethod
    def new_cli_app(cls, args: List[str]) -> Cli:
        parsed_args = Cli.parse_args(*args)
        app = new_application(
            chosen_files=parsed_args.chosen_files,
            output_dir=parsed_args.output_dir,
            skip_hidden=parsed_args.skip_hidden,
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

    def full_statistics_flow(self, chosen_files: List[Path]) -> int:
        return self.app.full_statistics(chosen_files)

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
            help="chose wheter you want to obtain basic funcionality or full statistics [basic_statistics, full_statistics]",
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

        namespace = parser.parse_args(args)

        file_paths: List[str] = list(namespace.chosen_files)
        for path in file_paths:
            if not (Path(path).is_file() or Path(path).is_dir()):
                raise ValueError(f"{path} doesn't exist!")

        return namespace
