import flet as ft
import polars as pl


def main(page: ft.Page):
    page.title = "Options"

    output = ft.Text()

    df = pl.read_excel(r"C:\Users\a002572\Desktop\Python\FileFlipper\config\codelist_SMHI_fileflipper.xlsx")
    datatype = df["DTYPE"].to_list()
    monitoring_programme = df["MPROG"].to_list()
    deliverer = df["LABO"].to_list()
    project = df["PROJ"].to_list()

    def get_options_datatype():
        options = []
        for d in datatype:
            if d is None:
                continue
            options.append(
                ft.DropdownOption(
                    text=d,
                )
            )

        return options

    def dropdown_selected_datatype(d):
        page.selected_datatype = d.control.value
        output.value = f"Selected datatype: {page.selected_datatype}"
        page.update()

    # ---- GUI ----
    page.add(
        ft.Column(
            [
                ft.Dropdown(
                    "Select datatype",
                    editable=True,
                    enable_filter=True,
                    label="Datatype",
                    options=get_options_datatype(),
                    on_change=dropdown_selected_datatype,
                ),
                output,
            ],
            spacing=15,
        )
    )


ft.app(target=main)
