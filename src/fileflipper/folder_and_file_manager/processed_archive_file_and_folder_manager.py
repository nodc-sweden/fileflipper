# Following script contains four classes performing actions related to checking content in initial delivered files folder,
# creating a folder to store the original received files (Originalfiler_från_leverantör) and copy the files the the
# originalarkiv-folder


import pathlib
import shutil


# This class has a method that checks if there is any content in the original archive folder.

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

    #     self._validate()
    #
    # def _validate(self):
    #     if not all([
    #         self._root_directory,
    #         self._archive_type,
    #         self._datatype,
    #         self._deliverer,
    #         self._year,
    #         self._project,
    #         self._shark_name
    #     ]):
    #         raise AttributeError("Missing input for subfolder!")

    @property
    def archive_directory(self) -> pathlib.Path:
        return self._root_directory / self._archive_type / self._datatype

    def get_new_archive_directory(self) -> pathlib.Path:
        path = self.archive_directory / f"SHARK_{self._datatype}_{self._year}_{self._deliverer}_{self._project}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    # Method add_files copies the files from originalarkivet and distributes them to the defined subfolders based on
    # datatype. If a file already exist in the subfolder, an action is required. Cancel will stop the process, Add will
    # add the file to the subfolder and if the new file has the same name as the old file, the file will be overwritten.
    # HOW DO WE WANT THIS? New files normally have new names, we only want one file in each subfolder, except for
    # correspondance where several emails are OK, but normally new emails have new names

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


# pathway = r"C:\Users\a002572\Desktop\Python\FileFlipper\Originalfiler\Phytoplankton\GU\2024\PROJ\received_202512011342"
# archive_directory = pathlib.Path(pathway)
# archive_directory_check = CheckOriginalArchiveDirectory(archive_directory).check_content()
# folders_bio = ProcessedArchiveDirectory(
#     root_directory=pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Arbetsmapp"), archive_type="datasets"
#     , datatype="Phytoplankton", year="2020", deliverer="GU", project="PROJ")
# data_bio = folders_bio.get_new_archive_directory()
# copy_files = folders_bio.add_files(archive_directory, data_bio)
# print(archive_directory)
# print(folders_bio)
# print(archive_directory_check)
# print(data_bio)
# print(copy_files)


class ProcessedArchiveDirectoryPhysChem(ProcessedArchiveDirectory):

    @property
    def archive_directory(self) -> pathlib.Path:
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
    ## -----------NOT SURE ABOUT THE SECTION BELOW-----------------------
    # return MAPPER.get(datatype.lower(), OriginalArchiveDirectory)(
    #     root_directory=root_directory,
    #     datatype=datatype,
    #     monitoring_programme=monitoring_programme,
    #     deliverer=deliverer,
    #     year=year,
    #     project=project,
    # )
    ## ------------------------------------------------------------------

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

# pathway = r"C:\Users\a002572\Desktop\Python\FileFlipper\Originalfiler\Phytoplankton\GU\2024\PROJ\received_202512011342"
# archive_directory = pathlib.Path(pathway)
# archive_directory_check = CheckOriginalArchiveDirectory(archive_directory).check_content()
# folders_physchem = ProcessedArchiveDirectoryPhysChem(
#    root_directory=pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Arbetsmapp"), archive_type=
#    "phy_che_validation", monitoring_programme="nationella_data", year="2021", deliverer="GU")
# val_path, fb_path, qc_path = folders_physchem.get_new_archive_directory()
# copied_files = folders_physchem.add_files(
#    source_dir=archive_directory,
#    target_dir=val_path
# )
# print(archive_directory)
# print(folders_physchem)
# print(archive_directory_check)
# print(val_path, fb_path, qc_path)
# print(copied_files)
