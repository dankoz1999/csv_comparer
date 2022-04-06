from pathlib import Path
from typing import List

from comparer.adapters.disk_repository import DiskRepository
from comparer.app import Application
from comparer.domain.repositories import FileRepository


def new_application(
    data_dir: Path,
    output_dir: Path,
    chosen_files: List[str],
    skip_hidden: bool = True,
    debug: bool = True,
) -> Application:
    file_repo = resolve_diagram_repo(
        data_dir, output_dir, chosen_files, skip_hidden, debug
    )

    return Application(file_repo=file_repo, debug=debug)


def resolve_diagram_repo(
    data_dir: Path,
    output_dir: Path,
    chosen_files: List[str],
    skip_hidden: bool = True,
    debug: bool = True,
) -> FileRepository:
    """
    creates the proper diagram repo based on the environment variables
    """
    # TODO later
    # if (
    #     AZURE_BLOB_CONTAINER is not None
    #     and AZURE_BLOB_CONNECTION_STRING is not None
    #     and AZURE_BLOB_CONNECTION_STRING != ""
    # ):
    #     # THOSE are intentionally read from environment variables to avoid passing them as arguments
    #     # and hardcoding anywhere in the code.
    #     container = AZURE_BLOB_CONTAINER
    #     connection_string = AZURE_BLOB_CONNECTION_STRING
    #     logger.info(
    #         f"creating a azure blob application with container: {container} @ {diagrams_dir}"
    #     )
    #     blob_structure = P44BlobStructure()
    #     return DiagramAzureBlobRepo(
    #         container,
    #         connection_string,
    #         blob_structure,
    #         working_directory=diagrams_dir,
    #     )
    # else:

    return DiskRepository(data_dir, output_dir, chosen_files, skip_hidden, debug)
