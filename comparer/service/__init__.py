from pathlib import Path
from typing import List

from adapters.disk_repository import DiskRepository
from app import Application
from domain.repositories import FileRepository


def new_application(
    chosen_files: List[str],
    output_dir: Path,
    skip_hidden: bool = True,
    debug: bool = True,
) -> Application:

    file_repo = DiskRepository(
        chosen_files=[Path(f) for f in chosen_files],
        output_dir=output_dir,
        skip_hidden=skip_hidden,
        debug=debug,
    )

    return Application(file_repo=file_repo, debug=debug)


def resolve_diagram_repo(
    chosen_files: List[str],
    output_dir: Path,
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

    return DiskRepository(chosen_files, output_dir, skip_hidden, debug)
