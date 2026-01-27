# The following script contain three classes performing actions related to checking content in initial delivered files
# folder, creating a folder in the processed data archive (Arbetsmappen) and copy the files to the correct subfolders
# based on file type in the arbetsmapp

import pathlib
import shutil


class CheckOriginalArchiveDirectory:
    def __init__(self, directory: pathlib.Path | str = None):
        self._directory = directory

    def check_content(self) -> list[str] | str:
        files = [str(file) for file in self._directory.iterdir() if file.is_file()]
        if files:
            return files
        else:
            return []


DEFAULT_EXTENSIONS = ['.msg', '.txt', '.xlsx', '.pdf', '.docx', '.xml', '.zip']
DEFAULT_FOLDER_MAPPING = {
    '.msg': 'correspondence',
    '.xlsx': 'received_data',
    '.txt': 'text_files',
    '.pdf': 'pdf_files',
    '.docx': 'documents',
    '.xml': 'received_data',
    '.zip': 'zip-files'
}


class ProcessedArchiveDirectory:
    def __init__(self,
                 root_directory: pathlib.Path = None,
                 archive_type: str = None,
                 monitoring_programme: str = None,
                 datatype: str = None,
                 deliverer: str = None,
                 year: str | int | list[int] | list[str] = None,
                 project: str = None,
                 shark_name: str = None
                 ):
        self._root_directory = pathlib.Path(root_directory)
        self._archive_type = archive_type
        self._monitoring_programme = monitoring_programme
        self._datatype = datatype
        self._deliverer = deliverer
        self._year = year
        self._project = project
        self._shark_name = shark_name

    @property
    def archive_directory(self) -> pathlib.Path:
        return self._root_directory / self._archive_type / self._datatype

    def get_new_archive_directory(self) -> pathlib.Path:
        path = self.archive_directory / f"SHARK_{self._datatype}_{self._year}_{self._deliverer}_{self._project}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def add_files(self, source_dir: pathlib.Path = None, target_dir: pathlib.Path = None) -> list[pathlib.Path]:
        copied_files = []
        for file in source_dir.iterdir():
            if file.is_file():

                ext = file.suffix.lower()
                subfolder_name = DEFAULT_FOLDER_MAPPING[ext]
                subfolder_path = target_dir / subfolder_name

                if not subfolder_path.exists():
                    print(f"Folder doesn't exist, will create subfolder: {subfolder_path}")
                    subfolder_path.mkdir(parents=True)
                target_file = subfolder_path / file.name

                if target_file.exists():
                    print(f"File already exist: {target_file}")
                    choice = input("Select action; [C]ancel, [A]dd (overwrites), [O]verwrite").strip().lower()

                    if choice == "C":
                        print("Cancel file copy")

                    elif choice == "A":
                        shutil.copy(file, target_dir)
                        copied_files.append(target_dir / file.name)
                        print("Adds file or overwrites existing file")

                    elif choice == "O":
                        print("Overwrite existing file")
                        try:
                            for f in target_file.parent.iterdir():
                                if f.is_file():
                                    f.unlink()
                            print("All existing files in destination folder deleted.")
                        except Exception as e:
                            print(f"Error deleting existing files: {e}")
                        try:
                            shutil.copy(file, target_dir)
                            copied_files.append(target_dir / file.name)
                        except Exception as e:
                            print(f"Error copying file: {e}")
                            return copied_files
                shutil.copy(file, target_file)
                copied_files.append(target_file)
                continue

            return copied_files


class ProcessedArchiveDirectoryPhysChem(ProcessedArchiveDirectory):

    @property
    def archive_directory(self) -> pathlib.Path:
        mapping = {
            "NAT_Data": "nationella_data",
            "PROJ_Data": "proj_data",
            "REG_RECIP_Data": "reg_recip_data",
        }

        self._monitoring_programme = mapping.get(
            self._monitoring_programme,
            self._monitoring_programme
        )

        return self._root_directory / self._archive_type / self._monitoring_programme / self._year / self._deliverer

    def get_new_archive_directory(self) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
        val_path = self.archive_directory / f"validering"
        val_path.mkdir(parents=True, exist_ok=True)
        fb_path = self.archive_directory / f"validering" / f"feedback" / f"lägg_gamla_filer_här"
        fb_path.mkdir(parents=True, exist_ok=True)
        qc_path = self.archive_directory / f"validering" / f"QC"
        qc_path.mkdir(parents=True, exist_ok=True)
        return val_path, qc_path, fb_path

    def add_files(self, source_dir: pathlib.Path = None, target_dir: pathlib.Path = None) -> list[pathlib.Path]:
        copied_files = []
        for file in source_dir.iterdir():
            if file.is_file():
                shutil.copy(file, target_dir)
                copied_files.append(target_dir / file.name)
        return copied_files


MAPPER = {
    "physicalchemical": ProcessedArchiveDirectoryPhysChem,
}


def get_archive_folder_object(
        root_directory: str = None,
        archive_type: str = None,
        datatype: str = None,
        monitoring_programme: str = None,
        deliverer: str = None,
        year: int | str = None,
        project: str = None,
):
    if archive_type.lower() in ("phy_che_validation"):
        return ProcessedArchiveDirectoryPhysChem(
            root_directory=root_directory,
            archive_type=archive_type,
            datatype=datatype,
            monitoring_programme=monitoring_programme,
            year=year,
            project=project,
        )
    else:
        return ProcessedArchiveDirectory(
            root_directory=root_directory,
            archive_type=archive_type,
            datatype=datatype,
            deliverer=deliverer,
            year=year,
            project=project,
        )
