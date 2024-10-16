import flet as ft
import time

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
import flet as ft
import math
import random
import google.generativeai as genai
import json
import os
import PIL.Image
import time
import threading
import base64
from io import BytesIO
import flet.canvas as cv
from collections import namedtuple

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
        # Aplicar el descuento del 15%
        if not self.keyboard and e.control == self.text_field_premio :
            self.keyboard = True
            self.page.floating_action_button = ft.FloatingActionButton(
                icon=ft.icons.KEYBOARD_HIDE,
                on_click=self.hide_keyboard
            )
            self.page.update()
        self.sonido.play()
        if self.text_field_premio.value == '' or int(self.text_field_premio.value) <= 0:
            self.valor_final.value = "Ingresa un premio"
            self.premio_display.value = "$0"
            self.boton_copiar.disabled = True
            self.premio_display.update()
            self.boton_copiar.update()
            # if e.control.data == "descuento":
            #     return
        else:
            # return
            self.boton_copiar.disabled = False
            self.boton_copiar.update()
        self.intervalo_display.value = "$" + str(int(self.intervalo_slider.value))
        self.intervalo_display.update()
        self.cuotas_display.value = str(int(self.cuotas_slider.value))
        self.cuotas_display.update()
        if self.text_field_premio.value == '':
            return

        discounted_value = int(float(self.text_field_premio.value) * (1 - self.descuento / 100))
        
        intervalo = int(self.intervalo_slider.value)
        # Redondear al múltiplo de 300 más cercano, siempre hacia arriba
        rounded_value = int(math.ceil(discounted_value / intervalo) * intervalo)

        # Asegurarse de que el valor redondeado no sea menor que el valor descontado
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
        # self.page.overlay.append(self.sb_copiado)
        
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
            divisions=19, # i need each division be by 50
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

        self.content = ft.Column(
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
        self.border_radius=10
        self.border=ft.border.all(1, ft.colors.BLACK12)
        self.bgcolor=ft.colors.PRIMARY_CONTAINER
        self.width=500
        self.padding=10


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


# import pythoncom  # Import pythoncom


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
        self.text = "Año de auto por patente"
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
