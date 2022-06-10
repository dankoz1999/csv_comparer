import tempfile
from pathlib import Path

from comparer.storage_repos.disk_repository import DiskRepository
from tests import TESTS_OUTPUT_DIR


def test_file_in_folder() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".csv", dir=tmpdirname)

        repo = DiskRepository(
            chosen_files=[Path(tmpdirname)],
            output_dir=TESTS_OUTPUT_DIR,
            skip_hidden=True,
        )

        files = repo.get_files()

        assert len(list(files)) == 1
        file_1.close()


def test_duplicated_files() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".csv", dir=tmpdirname)

        repo = DiskRepository(
            chosen_files=[Path(tmpdirname), Path(tmpdirname)],
            output_dir=TESTS_OUTPUT_DIR,
            skip_hidden=True,
        )

        files = repo.get_files()

        assert len(list(files)) == 1
        file_1.close()


def test_path_is_file() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".csv", dir=tmpdirname)

        repo = DiskRepository(
            chosen_files=[Path(file_1.name)],
            output_dir=TESTS_OUTPUT_DIR,
            skip_hidden=True,
        )

        files = repo.get_files()

        assert len(list(files)) == 1
        file_1.close()


def test_empty_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".csv", dir=tmpdirname)

        repo = DiskRepository(
            chosen_files=[], output_dir=TESTS_OUTPUT_DIR, skip_hidden=True
        )
        files = repo.get_files()
        assert len(list(files)) == 0
        file_1.close()


# python -m pytest tests/test_file_repo.py
