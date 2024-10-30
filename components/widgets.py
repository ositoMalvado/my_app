import flet as ft
import time, math, random


class Billetes(ft.Container):
    billetes = [
        10, 20, 50, 100, 200, 500, 1000, 2000, 10000
    ]

    def update_total(self):
        total = 0
        for billete in self.billetes:
            if self.text_fields[billete].value:
                total += int(self.text_fields[billete].value) * billete
            self.total_final.value = f"Total: ${str(total)}"
            self.total_final.update()
            if total > 0:
                self.clear_all_button.visible = True
                self.send_button.visible = True
                self.clear_all_button.update()
                self.send_button.update()
            else:
                self.clear_all_button.visible = False
                self.send_button.visible = False
                self.clear_all_button.update()
                self.send_button.update()

    def on_change_billete(self, e):
        valor = int(e.control.data)
        if not e.control.value:
            self.totales[valor].value = f"= $0"
            self.totales[valor].update()
            self.update_total()
            return
        cantidad = int(e.control.value)
        self.totales[valor].value = f"= ${str(int(cantidad * valor))}"
        self.totales[valor].update()
        self.update_total()

    def clear_all_tf(self, e):
        for billete in self.billetes:
            self.text_fields[billete].value = ""
            self.totales[billete].value = f"= $0"
            self.text_fields[billete].update()
            self.totales[billete].update()
        self.update_total()

    def clear_tf(self, e):
        self.text_fields[int(e.control.data)].value = ""
        self.totales[int(e.control.data)].value = f"= $0"
        self.text_fields[int(e.control.data)].update()
        self.totales[int(e.control.data)].update()
        self.update_total()


    def send_total(self, e):
        total = 0
        for billete in self.billetes:
            if self.text_fields[billete].value:
                total += int(self.text_fields[billete].value) * billete
        self.page.launch_url(f"whatsapp://send?phone=2994516661&text=Total en efectivo: ${total}")


    def close_keyboard(self, e):
        for billete in self.billetes:
            self.text_fields[billete].disabled = True
        self.update()
        for billete in self.billetes:
            self.text_fields[billete].disabled = False
        self.update()
        

    def __init__(self):
        super().__init__()
        self.padding = 20
        self.border_radius = 10
        self.margin = 20
        self.bgcolor = ft.colors.SURFACE_VARIANT
        # self.bgcolor = ft.colors.PRIMARY_CONTAINER
        self.totales = {
            billete: ft.Text("= $0", width=100, size=16)
            for billete in self.billetes
        }
        self.total_final = ft.Text("Total: $0", size=24, weight=ft.FontWeight.BOLD)
        
        self.text_fields = {
            billete: ft.TextField(label=f"", height=40, content_padding=3, input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self.on_change_billete,
            data=str(billete),
            width=80,
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix=ft.Container(
                padding=ft.padding.only(right=5),
                content=ft.IconButton(
                    ft.icons.CLEAR,
                    on_click=self.clear_tf,
                    data=str(billete),
                    padding=0,
                    icon_size=15,
                    width=20,
                    height=20,
                )
            )
            )
            for billete in self.billetes
        }
        self.send_button = ft.IconButton(
            ft.icons.SEND,
            on_click=self.send_total,
            visible=False
        )
        self.clear_all_button = ft.IconButton(
            ft.icons.CLEAR_ALL,
            on_click=self.clear_all_tf,
            visible=False
        )
        self.content = ft.GestureDetector(
            on_tap=self.close_keyboard,
            content=ft.Column(
                [
                    ft.Stack(
                        [
                            ft.Row(
                                [
                                    self.total_final,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [
                                    self.clear_all_button,
                                    self.send_button
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            )
                        ],
                    ),
                    ft.Column(
                        [
                            ft.ListView(
                                [
                                    ft.ListTile(
                                        leading=ft.Row(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.ATTACH_MONEY),
                                                        ft.Text(f"{billete}", size=20, weight=ft.FontWeight.BOLD)
                                                    ],
                                                    width=120
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.Text("x", size=20, weight=ft.FontWeight.BOLD),
                                                        ft.Container(
                                                            self.text_fields[billete],
                                                            padding=ft.padding.only(left=10, right=10)
                                                        ),
                                                        self.totales[billete]
                                                    ],
                                                    expand=True,
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                                )
                                            ],
                                            spacing=0,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        content_padding=0,
                                    )
                                    for billete in self.billetes
                                ]
                            )
                        ],
                        expand=True,
                        scroll="auto"
                    )
                ]
            ),
        )

class Widget(ft.Container):

    def did_mount(self):
        self.page.run_thread(self.update_time)
        
        return super().did_mount()
    
    def will_unmount(self):
        self.working = False
        return super().will_unmount()

    def update_time(self):
        self.working = True
        if self.working:
            while True:
                time.sleep(1)
                self.initial_time += 1
                self.timer_text.value = str(self.initial_time)
                self.timer_text.update()

    def __init__(self):
        super().__init__()
        self.initial_time = 0
        self.timer_text = ft.Text(str(self.initial_time))
        self.content = ft.ListView(
            [
                ft.ListTile(
                    title=self.timer_text,
                    subtitle=ft.Text("Subtitle 1"),
                    leading=ft.Icon(ft.icons.PIN_DROP),
                ),
            ]
        )

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
                ft.DataColumn(ft.Text(expand=True,value="Ramo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text(expand=True,value="%SA", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text(expand=True,value="Mínimo", weight=ft.FontWeight.BOLD)),
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

class Zoomtainer(ft.Container):


    def zoom_hover(self, e):
        self.scale = self.zoom if e.data == "true" else 1
        self.update()


    def __init__(self, contenido, zoom):
        super().__init__()
        self.content = contenido
        self.scale = 1
        self.zoom = zoom
        self.animate_scale = ft.Animation(duration=100, curve=ft.AnimationCurve.FAST_OUT_SLOWIN)
        self.on_hover = self.zoom_hover    


class CalculadoraPremio(ft.Container):


    def hide_keyboard(self,e ):
        if not self.page.platform == ft.PagePlatform.IOS:
            return
        self.text_field_premio.disabled = True
        self.text_field_premio.update()
        time.sleep(0.01)
        self.page.floating_action_button = None
        if self.text_field_premio.value == '' or int(self.text_field_premio.value) <= 0:
            self.boton_copiar.disabled = True
        self.text_field_premio.disabled = False
        self.text_field_premio.update()
        self.boton_copiar.update()
        self.page.update()
        self.keyboard = False

    def update_premio(self, e):
        if self.text_field_premio.value == '' or int(self.text_field_premio.value) <= 0:
            self.valor_final.value = "Ingresa un premio"
            self.premio_display.value = "$0"
            self.boton_copiar.disabled = True
            self.premio_display.update()
            self.boton_copiar.update()
        else:
            self.boton_copiar.disabled = False
            self.boton_copiar.update()
        self.intervalo_display.value = "$" + str(int(self.intervalo_slider.value))
        self.intervalo_display.update()
        self.cuotas_display.value = str(int(self.cuotas_slider.value))
        self.cuotas_display.update()
        if self.text_field_premio.value == '':
            return
        self.sonido.play()
        discounted_value = int(float(self.text_field_premio.value) * (1 - self.descuento / 100))
        
        intervalo = int(self.intervalo_slider.value)
        
        rounded_value = int(math.ceil(discounted_value / intervalo) * intervalo)

        
        final_value = max(rounded_value, math.ceil(discounted_value))
        self.copy_value = final_value
        self.premio_display.value = "$" + str(int(final_value))
        self.premio_display.update()
        self.valor_final.value = str(int(self.cuotas)) + " cuotas de $" + str(int(final_value/self.cuotas))
        self.valor_final.update()

    def slider_handle(self, e):
        if e.control.data == "descuento":
            self.descuento = self.slider.value
            self.descuento_display.value = str(int(self.descuento)) + "%"
            self.descuento_display.update()
            self.slider.label = "Descuento: " + str(int(self.descuento)) + "%"
            self.slider.update()
        elif e.control.data == "cuotas":
            self.cuotas = self.cuotas_slider.value
            self.cuotas_slider.label = "Cuotas: " + str(int(self.cuotas))
            self.cuotas_slider.update()
        else:
            self.intervalo = self.intervalo_slider.value
            self.intervalo_slider.label = "Intervalo: $" + str(int(self.intervalo_slider.value))
            self.intervalo_slider.update()
        self.update_premio(e)
        self.sonido.play()

    def copy_premio(self, e):
        self.copy_sound.play()
        
        self.page.set_clipboard(str(self.copy_value))
        self.page.open(self.sb_copiado)
        self.page.update()

    def did_mount(self):
        
        
        self.page.overlay.append(self.sonido)
        self.page.overlay.append(self.copy_sound)
        self.page.update()
        return super().did_mount()

    def __init__(self):
        super().__init__()
        self.keyboard = False
        self.sonido = ft.Audio(src="pop2.mp3")
        self.copy_sound = ft.Audio(src="bubble.mp3")

        self.sb_copiado = ft.SnackBar(
            content=ft.Text("Premio copiado"),
            bgcolor=ft.colors.GREEN,
            duration=800
        )



        self.border_radius=10
        self.border=ft.border.all(1, ft.colors.BLACK12)
        self.bgcolor=ft.colors.PRIMARY_CONTAINER
        self.width=400
        self.margin = ft.margin.all(10)
        self.padding=ft.padding.all(10)
        self.bgcolor=ft.colors.SURFACE_VARIANT
        self.border_radius=10

        self.descuento = 15
        self.copy_value = 0

        self.slider = ft.Slider(
            value=self.descuento,
            min=0,
            max=15,
            divisions=15,
            on_change=self.slider_handle,
            label="Descuento: 15%",
            data="descuento",
        )

        self.valor_final = ft.Text("Ingresa un premio", expand=True, text_align=ft.TextAlign.CENTER)

        self.text_field_premio = ft.TextField(
            label="Premio",
            prefix_icon=ft.icons.ATTACH_MONEY_ROUNDED,
            hint_text="Ingresa el premio",
            height=40,
            content_padding=5,
            on_change=self.update_premio,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_focus=self.update_premio,
            input_filter = ft.NumbersOnlyInputFilter()
        )
        self.boton_copiar = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.ATTACH_MONEY_ROUNDED),
                    self.valor_final,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tooltip="Copiar premio con descuento",
            on_click=self.copy_premio,
            disabled=True,
        )

        self.descuento_display = ft.Text(str(self.descuento) + "%", weight=ft.FontWeight.BOLD)

        self.intervalo = 300
        self.intervalo_slider = ft.Slider(
            value=self.intervalo,
            min=50,
            max=1000,
            divisions=19, 
            on_change=self.slider_handle,
            label="Intervalo: 300",
            data="intervalo"
        )
        self.intervalo_display = ft.Text("$" + str(self.intervalo), weight=ft.FontWeight.BOLD)

        self.cuotas = 3
        self.cuotas_display = ft.Text(str(self.cuotas), weight=ft.FontWeight.BOLD)
        self.premio_display = ft.Text("$0", weight=ft.FontWeight.BOLD)
        self.cuotas_slider = ft.Slider(
            value=self.cuotas,
            min=1,
            max=6,
            divisions=5,
            on_change=self.slider_handle,
            label="Cuotas: " + str(self.cuotas),
            data="cuotas"
        )
        pointer = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Calculadora de Premio", weight=ft.FontWeight.BOLD, expand=True),
                self.text_field_premio,
                
                ft.Row(
                    [
                        ft.Text("Premio con descuento: ", weight=ft.FontWeight.BOLD),
                        self.premio_display,
                    ],
                    expand=True
                ),
                self.boton_copiar,
                ft.Row(
                    [
                        ft.Text("Descuento: ", weight=ft.FontWeight.BOLD),
                        self.descuento_display,
                    ],
                    expand=True
                ),
                self.slider,
                ft.Row(
                    [
                        ft.Text("Intervalo: ", weight=ft.FontWeight.BOLD),
                        self.intervalo_display,
                    ],
                    expand=True
                ),
                self.intervalo_slider,
                ft.Row(
                    [
                        ft.Text("Cuotas: ", weight=ft.FontWeight.BOLD),
                        self.cuotas_display,
                    ],
                    expand=True
                ),
                self.cuotas_slider,
                
            ],
            spacing=2,
            expand=True
        )
        if False:
            pointer = ft.TransparentPointer(
                content=pointer
            )
        self.content = ft.Stack(
            expand=True,
            controls=[
                ft.GestureDetector(
                    on_double_tap=lambda _: self.hide_keyboard(None),
                ),
                pointer
            ]
        )


class ColorButton(ft.IconButton):

    def did_mount(self):
        if not self.page.theme:
            self.page.theme = ft.Theme(
                color_scheme_seed="#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )
            self.page.update()
        return super().did_mount()

    def change_color(self, e):
        random_color = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.page.theme.color_scheme_seed = random_color
        self.page.update()

    def __init__(self):
        super().__init__()
        self.icon = ft.icons.PALETTE_ROUNDED
        self.tooltip = "Cambiar color"
        self.on_click = self.change_color





class ThemeButton(ft.IconButton):

    def change_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        self.icon = ft.icons.LIGHT_MODE_ROUNDED if self.page.theme_mode == ft.ThemeMode.DARK else ft.icons.DARK_MODE_ROUNDED
        self.page.update()

    def __init__(self):
        super().__init__()
        self.icon = ft.icons.DARK_MODE_ROUNDED
        self.tooltip = "Modo oscuro"
        self.on_click = self.change_theme





class TabGeneralPatentes(ft.Tab):

    patentes = {
        "AG450AA": "Enero 2024",
        "AG300AA": "Octubre 2023",
        "AG000AA": "Mayo 2023",
        "AF770AA": "Enero 2023",
        "AF600AA": "Octubre 2022",
        "AF000AA": "Agosto 2021",
        "AE600AA": "Enero 2021",
        "AE100AA": "Enero 2020",
        "AE000AA": "Octubre 2019",
        "AD400AA": "Enero 2019",
        "AD000AA": "Julio 2018",
        "AC200AA": "Enero 2018",
        "AC000AA": "Noviembre 2017",
        "AB000AA": "Febrero 2017",
        "AA900AA": "Enero 2017",
        "AA000AA": "Abril 2016",
        "PMA000": "2016",
        "ONA000": "2015",
        "NMA000": "2014",
        "MBA000": "2013",
        "KUA000": "2012",
        "JNA000": "2011",
        "IMA000": "2010",
        "HTA000": "2009",
        "GVA000": "2008",
        "GBA000": "2007",
        "FIA000": "2006",
        "ETA000": "2005",
        "EIA000": "2004",
        "EDA000": "2003",
        "DXA000": "2002",
        "DOA000": "2001",
        "DCA000": "2000",
        "CMA000": "1999",
        "BUA000": "1998",
        "BDA000": "1997",
        "APA000": "1996",
        "AAA000": "1995",
    }

    def __init__(self):
        super().__init__()
        self.text = "Año patente"
        self.mi_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Patente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Año", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
        for i, patente in enumerate(self.patentes):
            self.mi_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(Zoomtainer(ft.Text(patente, weight=ft.FontWeight.BOLD), zoom=1.2)),
                        ft.DataCell(Zoomtainer(ft.Text(self.patentes[patente]), zoom=1.2)),
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
