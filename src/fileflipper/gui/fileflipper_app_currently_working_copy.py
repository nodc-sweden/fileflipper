import flet as ft
import pathlib

from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import OriginalArchiveDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import (
    OriginalArchiveDirectoryPhysChemProfile)
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import ProcessedArchiveDirectory
from fileflipper.folder_and_file_manager.processed_archive_file_and_folder_manager import (
    ProcessedArchiveDirectoryPhysChem)
from config import DTYPE, ARCTYPE, LABO, YEAR, PROJ, MPROG


def main(page: ft.Page):
    page.title = "FileFlipper"

    selected_ini_dir = {"path": None}
    selected_orig_dir = {"path": None}
    selected_proc_dir = {"path": None}
    selected_archive = {"value": None}
    selected_datatype = {"value": None}
    selected_monitoring_programme = {"value": None}
    selected_deliverer = {"value": None}
    selected_project = {"value": None}
    selected_year = {"value": None}
    output = ft.Text()

    def select_ini_directory(folder: ft.FilePickerResultEvent):
        if folder.path:
            selected_ini_dir["path"] = pathlib.Path(folder.path)
            output.value = f"Selected initial directory: \n{folder.path}"
            page.update()

    file_content_ini = ft.FilePicker(on_result=select_ini_directory)
    page.overlay.append(file_content_ini)

    def select_orig_directory(folder: ft.FilePickerResultEvent):
        if folder.path:
            selected_orig_dir["path"] = pathlib.Path(folder.path)
            output.value = f"Selected original archive directory: \n{folder.path}"
            page.update()

    file_content_orig = ft.FilePicker(on_result=select_orig_directory)
    page.overlay.append(file_content_orig)

    def select_proc_directory(folder: ft.FilePickerResultEvent):
        if folder.path:
            selected_proc_dir["path"] = pathlib.Path(folder.path)
            output.value = f"Selected processed archive directory: \n{folder.path}"
            page.update()

    file_content_proc = ft.FilePicker(on_result=select_proc_directory)
    page.overlay.append(file_content_proc)

    def get_options_archive():
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

    def get_options_datatype():
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

    def get_options_monitoring_programme():
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

    def get_options_deliverer():
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

    def get_options_project():
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

    def get_options_year():
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

    def dropdown_selected_archive(a):
        selected_archive["value"] = a.control.value
        output.value = f"Selected archive: {selected_archive['value']}"
        page.update()

    def dropdown_selected_datatype(d):
        selected_datatype["value"] = d.control.value
        output.value = f"Selected datatype: {selected_datatype['value']}"
        page.update()

    def dropdown_selected_monitoring_programme(d):
        selected_monitoring_programme["value"] = d.control.value
        output.value = f"Selected monitoring_programme: {selected_monitoring_programme['value']}"
        page.update()

    def dropdown_selected_deliverer(d):
        selected_deliverer["value"] = d.control.value
        output.value = f"Selected deliverer: {selected_deliverer['value']}"
        page.update()

    def dropdown_selected_project(d):
        selected_project["value"] = d.control.value
        output.value = f"Selected project: {selected_project['value']}"
        page.update()

    def dropdown_selected_year(d):
        selected_year["value"] = d.control.value
        output.value = f"Selected year: {selected_year['value']}"
        page.update()

    def run_orig_directory(folder):
        orig_dir = OriginalArchiveDirectory(
            root_directory=selected_orig_dir["path"],
            datatype=selected_datatype["value"], deliverer=selected_deliverer["value"], year=selected_year["value"],
            project=selected_project["value"])
        new_folder = orig_dir.get_new_received_directory()

        if new_folder:
            output.value = "Found/created the following folder:\n" + str(new_folder)
        else:
            output.value = "No folder found/created"

        files = orig_dir.add_files(selected_ini_dir["path"], new_folder)

        if files:
            output.value = "Copied the following files:\n" + str(files)
        else:
            output.value = "No files found"

        page.update()

    def run_orig_directory_physchemprof(folder):
        orig_dir = OriginalArchiveDirectoryPhysChemProfile(
            root_directory=selected_orig_dir["path"], datatype=selected_datatype["value"],
            monitoring_programme=selected_monitoring_programme["value"], deliverer=selected_deliverer["value"],
            year=selected_year["value"], project=selected_project["value"])
        new_folder = orig_dir.get_new_received_directory()

        if new_folder:
            output.value = "Found/created the following folder:\n" + str(new_folder)
        else:
            output.value = "No folder found/created"

        files = orig_dir.add_files(selected_ini_dir["path"], new_folder)

        if files:
            output.value = "Copied the following files:\n" + str(files)
        else:
            output.value = "No files found"

        page.update()

    def run_proc_directory(folder):
        orig_dir = ProcessedArchiveDirectory(
            root_directory=selected_proc_dir["path"], archive_type=selected_archive["value"],
            datatype=selected_datatype["value"], deliverer=selected_deliverer["value"], year=selected_year["value"],
            project=selected_project["value"])
        new_folder = orig_dir.get_new_archive_directory()

        if new_folder:
            output.value = "Found/created the following folder:\n" + str(new_folder)
        else:
            output.value = "No folder found/created"

        files = orig_dir.add_files(selected_ini_dir["path"], new_folder)

        if files:
            output.value = "Copied the following files:\n" + str(files)
        else:
            output.value = "No files found"

        page.update()

    def run_proc_directory_physchemprof(folder):
        orig_dir = ProcessedArchiveDirectoryPhysChem(
            root_directory=selected_proc_dir["path"], archive_type=selected_archive["value"],
            datatype=selected_datatype["value"],
            monitoring_programme=selected_monitoring_programme["value"], deliverer=selected_deliverer["value"],
            year=selected_year["value"], project=selected_project["value"])
        val_path, fb_path, qc_path = orig_dir.get_new_archive_directory()

        if val_path:
            output.value = "Found/created the following folder:\n" + str(val_path)
        else:
            output.value = "No folder found/created"

        if fb_path:
            output.value = "Found/created the following folder:\n" + str(fb_path)
        else:
            output.value = "No folder found/created"

        if qc_path:
            output.value = "Found/created the following folder:\n" + str(qc_path)
        else:
            output.value = "No folder found/created"

        files = orig_dir.add_files(selected_ini_dir["path"], val_path)

        if files:
            output.value = "Copied the following files:\n" + str(files)
        else:
            output.value = "No files found"

        page.update()

    btn_select_ini_directory = ft.ElevatedButton(
        "Select initial directory",
        on_click=lambda _: file_content_ini.get_directory_path(),
    )

    btn_select_orig_directory = ft.ElevatedButton(
        "Select original archive directory",
        on_click=lambda _: file_content_orig.get_directory_path(),
    )

    row_directory = ft.Row([btn_select_ini_directory,
                            btn_select_orig_directory]
                           )

    btn_select_archive = ft.Dropdown(
        "Select archive",
        editable=True,
        enable_filter=True,
        label="Archive",
        options=get_options_archive(),
        on_change=dropdown_selected_archive,
    )

    btn_select_datatype = ft.Dropdown(
        "Select datatype",
        editable=True,
        enable_filter=True,
        label="Datatype",
        options=get_options_datatype(),
        on_change=dropdown_selected_datatype,
    )

    btn_select_monitoring_programme = ft.Dropdown(
        "Select monitoring programme",
        editable=True,
        enable_filter=True,
        label="Monitoring programme",
        options=get_options_monitoring_programme(),
        on_change=dropdown_selected_monitoring_programme,
    )

    btn_select_deliverer = ft.Dropdown(
        "Select deliverer",
        editable=True,
        enable_filter=True,
        label="Deliverer",
        options=get_options_deliverer(),
        on_change=dropdown_selected_deliverer,
    )

    btn_select_project = ft.Dropdown(
        "Select project",
        editable=True,
        enable_filter=True,
        label="Project",
        options=get_options_project(),
        on_change=dropdown_selected_project,
    )

    btn_select_year = ft.Dropdown(
        "Select year",
        editable=True,
        enable_filter=True,
        label="Year",
        options=get_options_year(),
        on_change=dropdown_selected_year,
    )

    row_options = ft.Row([btn_select_datatype,
                          btn_select_monitoring_programme,
                          btn_select_deliverer,
                          btn_select_project,
                          btn_select_year]
                         )

    # ---- GUI ----
    page.add(
        ft.Column(
            [
                row_directory,
                row_options,
                ft.ElevatedButton(
                    "Create original archive directory",
                    on_click=run_orig_directory,
                ),
                ft.ElevatedButton(
                    "Create original archive directory physicalchemical or profile",
                    on_click=run_orig_directory_physchemprof,
                ),
                ft.Container(height=30),
                ft.ElevatedButton(
                    "Select processed archive directory",
                    on_click=lambda _: file_content_proc.get_directory_path(),
                ),
                ft.Dropdown(
                    "Select archive",
                    editable=True,
                    enable_filter=True,
                    label="Archive",
                    options=get_options_archive(),
                    on_change=dropdown_selected_archive,
                ),
                ft.ElevatedButton(
                    "Create processed archive directory",
                    on_click=run_proc_directory,
                ),
                ft.ElevatedButton(
                    "Create processed archive directory physicalchemical or profile",
                    on_click=run_proc_directory_physchemprof,
                ),
                output,
            ],
            spacing=15,
        )
    )


ft.app(target=main)
