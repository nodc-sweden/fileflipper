import flet as ft
import polars as pl
import pathlib
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import InitialReceivedDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import OriginalArchiveDirectory
from fileflipper.folder_and_file_manager.original_archive_file_and_folder_manager import (
    OriginalArchiveDirectoryPhysChemProfile)


def main(page: ft.Page):
    page.title = "FileFlipper"

    selected_ini_dir = {"path": None}
    selected_orig_dir = {"path": None}
    output = ft.Text()

    # Dessa funkar:

    def select_ini_directory(folder: ft.FilePickerResultEvent):
        if folder.path:
            selected_ini_dir["path"] = pathlib.Path(folder.path)
            output.value = f"Selected directory: \n{folder.path}"
            page.update()

    file_content = ft.FilePicker(on_result=select_ini_directory)
    page.overlay.append(file_content)

    def select_orig_directory(folder: ft.FilePickerResultEvent):
        if folder.path:
            selected_orig_dir["path"] = pathlib.Path(folder.path)
            output.value = f"Selected archive directory: \n{folder.path}"
            page.update()

    file_content_orig = ft.FilePicker(on_result=select_orig_directory)
    page.overlay.append(file_content_orig)

    def run_initial(folder):
        if not selected_ini_dir["path"]:
            output.value = "No directory selected"
            page.update()
            return

        checker = InitialReceivedDirectory(selected_ini_dir["path"])
        files = checker.check_content()

        if files:
            output.value = "Found the following files:\n" + "\n".join(files)
        else:
            output.value = "No files found"

        page.update()

    def run_orig_directory(folder):
        orig_dir = OriginalArchiveDirectory(root_directory=pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Originalfiler"),
                                            datatype="Phytoplankton", deliverer="GU", year="2024", project="PROJ")
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
            root_directory=pathlib.Path(r"C:\Users\a002572\Desktop\Python\FileFlipper\Originalfiler"),
            datatype="PhysicalChemical", monitoring_programme="NAT_Data", deliverer="GU", year="2024", project="PROJ")
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

    # Till hit.

    # ---- GUI ----
    page.add(
        ft.Column(
            [
                ft.ElevatedButton(
                    "Select directory",
                    on_click=lambda _: file_content.get_directory_path(),
                ),
                ft.ElevatedButton(
                    "Initial directory check",
                    on_click=run_initial,
                ),
                ft.ElevatedButton(
                    "Select original directory",
                    on_click=lambda _: file_content_orig.get_directory_path(),
                ),
                ft.ElevatedButton(
                    "Create original archive directory",
                    on_click=run_orig_directory,
                ),
                ft.ElevatedButton(
                    "Create original archive directory physicalchemical or profile",
                    on_click=run_orig_directory_physchemprof,
                ),
                output,
            ],
            spacing=15,
        )
    )


ft.app(target=main)
