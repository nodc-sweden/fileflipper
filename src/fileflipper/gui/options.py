import flet as ft
import polars as pl
from config import DTYPE, ARCTYPE, LABO, YEAR, PROJ, MPROG


class OptionsDropDown:

    def __init__(self):
        self.output = None
        self.control = None
        self.page = None
        self.selected_archive = {"value": None}
        self.selected_datatype = {"value": None}
        self.selected_monitoring_programme = {"value": None}
        self.selected_deliverer = {"value": None}
        self.selected_project = {"value": None}
        self.selected_year = {"value": None}

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

        self.page.add(
            ft.Column(
                [
                    ft.Dropdown(
                        "Select archive",
                        editable=True,
                        enable_filter=True,
                        label="Archive",
                        options=self.get_options_archive(),
                        on_change=self.dropdown_selected_archive,
                    ),
                    ft.Dropdown(
                        "Select datatype",
                        editable=True,
                        enable_filter=True,
                        label="Datatype",
                        options=self.get_options_datatype(),
                        on_change=self.dropdown_selected_datatype,
                    ),
                    ft.Dropdown(
                        "Select monitoring programme",
                        editable=True,
                        enable_filter=True,
                        label="Monitoring programme",
                        options=self.get_options_monitoring_programme(),
                        on_change=self.dropdown_selected_monitoring_programme,
                    ),
                    ft.Dropdown(
                        "Select deliverer",
                        editable=True,
                        enable_filter=True,
                        label="Deliverer",
                        options=self.get_options_deliverer(),
                        on_change=self.dropdown_selected_deliverer,
                    ),
                    ft.Dropdown(
                        "Select project",
                        editable=True,
                        enable_filter=True,
                        label="Project",
                        options=self.get_options_project(),
                        on_change=self.dropdown_selected_project,
                    ),
                    self.output,
                ],
                spacing=15
            )
        )
