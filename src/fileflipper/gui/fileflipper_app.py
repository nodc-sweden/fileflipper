import flet as ft
import polars as pl
import pathlib
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import InitialReceivedDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import OriginalArchiveDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import (
    OriginalArchiveDirectoryPhysChemProfile)
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import CheckOriginalArchiveDirectory
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import ProcessedArchiveDirectory
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import (
    ProcessedArchiveDirectoryPhysChem)
from src.fileflipper.gui.config import DTYPE, ARCTYPE, LABO, YEAR, PROJ, MPROG


class FileFlipperGUI:

    def __init__(self):
        self.page = None
        self._selected_ini_dir: None | pathlib.Path = None
        self._selected_orig_dir: None | pathlib.Path = None
        self.output = None
        self.control = None
        self.selected_archive = None
        self.selected_datatype = None
        self.selected_monitoring_programme = None
        self.selected_deliverer = None
        self.selected_project = None
        self.selected_year = None
        self.app = ft.app(target=self.main)

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = f"FileFlipper"
        self.page.window_height = 1000
        self.page.window_width = 1200
        self._build()

    def _on_select_ini_directory(self, *args):
        self._btn_select_ini_directory.bgcolor = "red"
        self._btn_select_ini_directory.update()
        self._file_content_ini.get_directory_path()

    def _on_select_orig_directory(self, *args):
        self._btn_select_orig_directory.bgcolor = "red"
        self._btn_select_orig_directory.update()
        self._file_content_orig.get_directory_path()

    def _build(self):
        self._output = ft.Text()

        self._file_content_ini = ft.FilePicker(on_result=self._select_ini_directory)
        self.page.overlay.append(self._file_content_ini)

        self._file_content_orig = ft.FilePicker(on_result=self._select_orig_directory)
        self.page.overlay.append(self._file_content_orig)

        self._btn_select_ini_directory = ft.ElevatedButton(
            "Select initial directory",
            on_click=self._on_select_ini_directory,
        )

        self._btn_select_orig_directory = ft.ElevatedButton(
            "Select original archive directory",
            on_click=self._on_select_orig_directory,
        )

        row_directory = ft.Row([self._btn_select_ini_directory,
                                self._btn_select_orig_directory]
                               )

        self._btn_select_archive = ft.Dropdown(
            "Select archive",
            editable=True,
            enable_filter=True,
            label="Archive",
            options=self.get_options_archive(),
            on_change=self.dropdown_selected_archive,
        )

        self._btn_select_datatype = ft.Dropdown(
            "Select datatype",
            editable=True,
            enable_filter=True,
            label="Datatype",
            options=self.get_options_datatype(),
            on_change=self.dropdown_selected_datatype,
        )

        self._btn_select_monitoring_programme = ft.Dropdown(
            "Select monitoring programme",
            editable=True,
            enable_filter=True,
            label="Monitoring programme",
            options=self.get_options_monitoring_programme(),
            on_change=self.dropdown_selected_monitoring_programme,
        )

        self._btn_select_deliverer = ft.Dropdown(
            "Select deliverer",
            editable=True,
            enable_filter=True,
            label="Deliverer",
            options=self.get_options_deliverer(),
            on_change=self.dropdown_selected_deliverer,
        )

        self._btn_select_project = ft.Dropdown(
            "Select project",
            editable=True,
            enable_filter=True,
            label="Project",
            options=self.get_options_project(),
            on_change=self.dropdown_selected_project,
        )

        self._btn_select_year = ft.Dropdown(
            "Select year",
            editable=True,
            enable_filter=True,
            label="Year",
            options=self.get_options_year(),
            on_change=self.dropdown_selected_year,
        )

        row_options = ft.Row([self._btn_select_datatype,
                              self._btn_select_monitoring_programme,
                              self._btn_select_deliverer,
                              self._btn_select_project,
                              self._btn_select_year]
                             )

        self.page.add(
            ft.Column(
                [
                    row_directory,
                    row_options,
                    ft.ElevatedButton(
                        "Create original archive directory",
                        on_click=self._run_orig_directory,
                    ),
                    ft.ElevatedButton(
                        "Create original archive directory physicalchemical or profile",
                        on_click=self._run_orig_directory_physchemprof,
                    ),
                    self._output,
                ],
                spacing=15,
            )
        )

    def update_page(self):
        self.page.update()

    def _select_ini_directory(self, folder: ft.FilePickerResultEvent):
        if not folder.path:
            return
        self._selected_ini_dir = pathlib.Path(folder.path)
        self._output.value = f"Selected initial directory: \n{folder.path}"
        self.update_page()

    def _select_orig_directory(self, folder: ft.FilePickerResultEvent):
        if not folder.path:
            return
        self._selected_orig_dir = pathlib.Path(folder.path)
        self._output.value = f"Selected archive directory: \n{folder.path}"
        self.update_page()

    def get_options_archive(self):
        options = []
        for a in ARCTYPE:
            if a is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=a,
                )
            )
        return options

    def get_options_datatype(self):
        options = []
        for d in DTYPE:
            if d is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=d,
                )
            )
        return options

    def get_options_monitoring_programme(self):
        options = []
        for mp in MPROG:
            if mp is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=mp,
                )
            )
        return options

    def get_options_deliverer(self):
        options = []
        for de in LABO:
            if de is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=de,
                )
            )
        return options

    def get_options_project(self):
        options = []
        for p in PROJ:
            if p is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=p,
                )
            )
        return options

    def get_options_year(self):
        options = []
        for y in YEAR:
            if y is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=y,
                )
            )
        return options

    def dropdown_selected_archive(self):
        self.selected_archive["value"] = self.control.value
        self.page.update()
        print(self.selected_datatype)

    def dropdown_selected_datatype(self):
        self.selected_datatype["value"] = self.control.value
        self.page.update()

    def dropdown_selected_monitoring_programme(self):
        self.selected_monitoring_programme["value"] = self.control.value
        self.page.update()

    def dropdown_selected_deliverer(self):
        self.selected_deliverer["value"] = self.control.value
        self.page.update()

    def dropdown_selected_project(self):
        self.selected_project["value"] = self.control.value
        self.page.update()

    def dropdown_selected_year(self):
        self.selected_year["value"] = self.control.value
        self.page.update()

    def _run_orig_directory(self, *args, **kwargs):
        orig_dir = OriginalArchiveDirectory(root_directory=pathlib.Path(self._selected_orig_dir),
                                            datatype=self.selected_datatype["value"],
                                            deliverer=self.selected_deliverer["value"],
                                            year=self.selected_year["value"],
                                            project=self.selected_project["value"])
        new_folder = orig_dir.get_new_received_directory()

        if new_folder:
            self._output.value = "Found/created the following folder:\n" + str(new_folder)
        else:
            self._output.value = "No folder found/created"

        files = orig_dir.add_files(self._selected_ini_dir, new_folder)

        if files:
            self._output.value = "Copied the following files:\n" + str(files)
        else:
            self._output.value = "No files found"

        self.update_page()

    def _run_orig_directory_physchemprof(self):
        orig_dir = OriginalArchiveDirectoryPhysChemProfile(root_directory=self._selected_orig_dir["path"],
                                                           datatype=self.selected_datatype["value"],
                                                           deliverer=self.selected_deliverer["value"],
                                                           year=self.selected_year["value"],
                                                           project=self.selected_project["value"])
        new_folder = orig_dir.get_new_received_directory()

        if new_folder:
            self._output.value = "Found/created the following folder:\n" + str(new_folder)
        else:
            self._output.value = "No folder found/created"

        files = orig_dir.add_files(self._selected_ini_dir, new_folder)

        if files:
            self._output.value = "Copied the following files:\n" + str(files)
        else:
            self._output.value = "No files found"

        self.update_page()

    # ---- FileFlipperGUI ----


if __name__ == "__main__":
    gui = FileFlipperGUI()
