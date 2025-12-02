from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import InitialReceivedDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import OriginalArchiveDirectory

import pathlib


class FileFlipperController:
    def __init__(self):
        self._initial_received_directory: InitialReceivedDirectory | None = None
        self._original_archive_directory: OriginalArchiveDirectory | None = None

    def set_received_folder(self, directory: str):
        self._initial_received_directory = InitialReceivedDirectory(directory=directory)

    def create_original_archive_directory(self, root_directory: pathlib.Path, datatype: str, monitoring_programme: str,
                                          deliverer: str, year: str | int | list[int] | list[str], project: str):
        self._original_archive_directory = OriginalArchiveDirectory(root_directory=root_directory, datatype=datatype,
                                                                    monitoring_programme=monitoring_programme,
                                                                    deliverer=deliverer, year=year, project=project)


