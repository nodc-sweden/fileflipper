# Following script contains four classes performing actions related to checking content in initial delivered files folder,
# creating a folder to store the original received files (Originalfiler_från_leverantör) and copy the files the the
# originalarkiv-folder


import datetime
import pathlib
import shutil


# This class has a method that checks if there is any content in the initial folder for received files.

class InitialReceivedDirectory:
    def __init__(self, directory: pathlib.Path | str = None):
        self._directory = directory

    def check_content(self) -> list[str] | str:
        files = [str(file) for file in self._directory.iterdir() if file.is_file()]
        if files:
            return files
        else:
            return []


def _get_year_str(year: str | int | list[int] | list[str]) -> str:
    if isinstance(year, str):
        return year


# This class contains several methods to create the correctly named and located originalarkiv-folder and copy the
# received files to this folder. The archive_directory is built to create the correct folder structure for biology
# data deliveries, the get_new_received_directory creates a subfolder in the correct folder namned "received_"+ datetime
# to be able to easy follow which deliveries are the latest. add_files then copies the content from the initial folder
# to the correct newly created subfolder. There are specific classes below for datatypes with other folder structures,
# for example profile and physcialchemical

class OriginalArchiveDirectory:
    def __init__(self,
                 root_directory: pathlib.Path = None,
                 datatype: str = None,
                 monitoring_programme: str = None,
                 deliverer: str = None,
                 year: str | int | list[int] | list[str] = None,
                 project: str = None,
                 ):
        self._root_directory = pathlib.Path(root_directory)
        self._datatype = datatype
        self._monitoring_programme = monitoring_programme
        self._deliverer = deliverer
        self._year = year
        self._project = project
        self._validate()

    def _validate(self):
        if not all([
            self._root_directory,
            self._datatype,
            self._deliverer,
            self._year,
            self._project
        ]):
            raise AttributeError("Missing input for subfolder!")

    @property
    def archive_directory(self) -> pathlib.Path:
        return self._root_directory / self._datatype / self._deliverer / self._year / self._project.upper()

    def get_new_received_directory(self) -> pathlib.Path:
        dtime = datetime.datetime.now().strftime("%Y%m%d%H%M")
        path = self.archive_directory / f"received_{dtime}"
        path.mkdir(parents=True)
        return path

    def add_files(self, source_dir: pathlib.Path = None, target_dir: pathlib.Path = None) -> list[pathlib.Path]:
        copied_files = []
        for file in source_dir.iterdir():
            if file.is_file():
                shutil.copy(file, target_dir)
                copied_files.append(target_dir / file.name)
        return copied_files


## -------------TEST SECTION START--------------------------------------------------------------
# initial_directory = pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Slask")
# initial_directory_check = InitialReceivedDirectory(initial_directory).check_content()
# folders_bio = OriginalArchiveDirectory(
#     root_directory=pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Originalfiler")
#     , datatype="Phytoplankton", deliverer="GU", year="2024", project="PROJ")
# data_bio = folders_bio.get_new_received_directory()
# copy_files = folders_bio.add_files(initial_directory, data_bio)
# print(initial_directory)
# print(folders_bio)
# print(initial_directory_check)
# print(data_bio)
# print(copy_files)
## -------------TEST SECTION END----------------------------------------------------------------


class OriginalArchiveDirectoryPhysChemProfile(OriginalArchiveDirectory):

    def _validate(self):
        if not all([
            self._root_directory,
            self._datatype,
            self._monitoring_programme,
            self._deliverer,
            self._year,
            self._project
        ]):
            raise AttributeError("Missing input for subfolder!")

    @property
    def archive_directory(self) -> pathlib.Path:
        return self._root_directory / self._datatype / self._monitoring_programme / self._year / self._project


MAPPER = {
    "profile": OriginalArchiveDirectoryPhysChemProfile,
    "physicalchemical": OriginalArchiveDirectoryPhysChemProfile,
}


def get_archive_folder_object(
        root_directory: str = None,
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

    if datatype.lower() in ("profile", "physicalchemical"):
        return OriginalArchiveDirectoryPhysChemProfile(
            root_directory=root_directory,
            datatype=datatype,
            monitoring_programme=monitoring_programme,
            year=year,
            project=project,
        )
    else:
        return OriginalArchiveDirectory(
            root_directory=root_directory,
            datatype=datatype,
            deliverer=deliverer,
            year=year,
            project=project,
        )
