from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import InitialReceivedDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import OriginalArchiveDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import \
    OriginalArchiveDirectoryPhysChemProfile
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import CheckOriginalArchiveDirectory
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import ProcessedArchiveDirectory
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import \
    ProcessedArchiveDirectoryPhysChem

import pathlib


class FileFlipperController:
    def __init__(self):
        self._initial_received_directory: InitialReceivedDirectory | None = None
        self._original_archive_directory: OriginalArchiveDirectory | None = None
        self._original_archive_directory_physchemprof: OriginalArchiveDirectoryPhysChemProfile | None = None
        self._check_original_archive_directory: CheckOriginalArchiveDirectory | None = None
        self._processed_archive_directory: ProcessedArchiveDirectory | None = None
        self._processed_archive_directory_physchem: ProcessedArchiveDirectoryPhysChem | None = None

    def set_received_folder(self, directory: str):
        self._initial_received_directory = InitialReceivedDirectory(directory=directory)

    def create_original_archive_directory(self, root_directory: pathlib.Path, datatype: str, monitoring_programme: str,
                                          deliverer: str, year: str | int | list[int] | list[str], project: str):
        self._original_archive_directory = OriginalArchiveDirectory(root_directory=root_directory, datatype=datatype,
                                                                    monitoring_programme=monitoring_programme,
                                                                    deliverer=deliverer, year=year, project=project)

    def create_original_archive_directory_physchemprof(self, root_directory: pathlib.Path, datatype: str,
                                                       monitoring_programme: str, deliverer: str,
                                                       year: str | int | list[int] | list[str], project: str):
        self._original_archive_directory_physchemprof = OriginalArchiveDirectoryPhysChemProfile(
            root_directory=root_directory, datatype=datatype, monitoring_programme=monitoring_programme,
            deliverer=deliverer, year=year, project=project)

    def check_original_archive_folder(self, directory: str):
        self._check_original_archive_directory = CheckOriginalArchiveDirectory(directory=directory)

    def create_processed_archive_directory(self, root_directory: pathlib.Path, archive_type: str,
                                           monitoring_programme: str, datatype: str, deliverer: str,
                                           year: str | int | list[int] | list[str], project: str, shark_name: str):
        self._processed_archive_directory = ProcessedArchiveDirectory(root_directory=root_directory,
                                                                      archive_type=archive_type, monitoring_programme=
                                                                      monitoring_programme, datatype=datatype, deliverer
                                                                      =deliverer, year=year, project=project, shark_name
                                                                      =shark_name)

    def create_processed_archive_directory_physchem(self, root_directory: pathlib.Path, archive_type: str,
                                                    monitoring_programme: str, datatype: str, deliverer: str,
                                                    year: str | int | list[int] | list[str], project: str,
                                                    shark_name: str):
        self._processed_archive_directory_physchem = ProcessedArchiveDirectoryPhysChem(root_directory=root_directory,
                                                                                       archive_type=archive_type,
                                                                                       monitoring_programme=
                                                                                       monitoring_programme,
                                                                                       datatype=datatype,
                                                                                       deliverer=deliverer,
                                                                                       year=year,
                                                                                       project=project,
                                                                                       shark_name=shark_name)
