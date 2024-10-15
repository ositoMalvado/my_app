import flet as ft
from controls import Zoomtainer
class TabFederacionFranquicias(ft.Tab):

    franquicias = [
        {"tipo": "Auto", "porcentaje": "1%", "Monto": "$300.000"},
        {"tipo": "Auto", "porcentaje": "2%", "Monto": "$400.000"},
        {"tipo": "Auto", "porcentaje": "4%", "Monto": "$500.000"},
        {"tipo": "Auto", "porcentaje": "6%", "Monto": "$630.000"},
        {"tipo": "Camiones", "porcentaje": "2%", "Monto": "$1.150.000"},
        {"tipo": "Acoplados", "porcentaje": "2%", "Monto": "$870.000"},
    ]


    def __init__(self):
        super().__init__()
        self.text = "Franquicias"
        self.mi_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(expand=True,value="Tipo de Vehículo", weight=ft.FontWeight.BOLD), tooltip="Tipo de Vehículo"),
                ft.DataColumn(ft.Text(expand=True,value="% Suma Asegurada", weight=ft.FontWeight.BOLD), tooltip="% Suma Asegurada"),
                ft.DataColumn(ft.Text(expand=True,value="Monto mínimo de Franquicia", weight=ft.FontWeight.BOLD), tooltip="Monto mínimo de Franquicia"),
            ],
            rows=[],
            expand=True,
        )

        for i, franquicia in enumerate(self.franquicias):
            self.mi_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(Zoomtainer(ft.Text(franquicia["tipo"], weight=ft.FontWeight.BOLD), zoom=1.5)),
                        ft.DataCell(Zoomtainer(ft.Text(franquicia["porcentaje"]), zoom=1.5)),
                        ft.DataCell(Zoomtainer(ft.Text(franquicia["Monto"]), zoom=1.5)),
                    ],
                    color=ft.colors.BLACK12 if i % 2 == 0 else None
                )
            )
        self.expand = True
        self.content = ft.Column(
            controls=[
                ft.Container(height=5),
                ft.Container(
                    self.mi_data_table,
                    border_radius=10,
                    border=ft.border.all(1, ft.colors.BLACK12),
                    bgcolor=ft.colors.PRIMARY_CONTAINER
                )
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll="auto",
            expand=True
        )