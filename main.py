import flet as ft
from components.widgets import *
from components.functions import *
import time
def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    page.title = "Utilidades"
    page.theme_mode = ft.ThemeMode.DARK
    page.locale_configuration = ft.LocaleConfiguration(
        [ft.Locale('es', 'ES')],
        current_locale=ft.Locale('es', 'ES'),
    )
    page.bgcolor = ft.colors.BACKGROUND
    last_width, last_height = calcular_alto(414)
    resizing = False
    def resize_task():
        nonlocal last_width, last_height, resizing
        if resizing:
            return
        if page.window.width == last_width and page.window.height == last_height:
            return
        resizing = True
        if page.window.width != last_width:
            ancho, alto = calcular_alto(ancho=page.window.width)
        else:
            ancho, alto = calcular_alto(alto=page.window.height)
        page.window.width, page.window.height = ancho, alto
        page.update()
        last_width, last_height = page.window.width, page.window.height
        time.sleep(0.5)
        resizing = False

    def on_resize(e):
        page.run_thread(resize_task)
    page.on_resized = on_resize
    page.window.width, page.window.height = calcular_alto(200)
    page.window.always_on_top = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    tabs = ft.Tabs(
        [
            ft.Tab(
                text="RUS",
                content=ft.Container(
                    expand=True,
                    content=ft.Tabs(
                        [
                            ft.Tab(
                                text="Premio",
                                content=CalculadoraPremio()
                            )
                        ],
                        tab_alignment=ft.TabAlignment.CENTER,
                        expand=True
                    ),

                )
            ),
            ft.Tab(
                text="GENERAL",
                content=ft.Container(
                    ft.Tabs(
                        [
                            TabGeneralPatentes(),
                            TabFederacionFranquicias(),
                        ],
                        tab_alignment=ft.TabAlignment.CENTER,
                        expand=True
                    ),
                    expand=True
                )
            ),
            ft.Tab(
                # text="FED",
                tab_content=ft.Icon(ft.icons.SETTINGS),
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ThemeButton(),
                                    ColorButton(),
                                ]
                            )
                        ],
                        expand=True
                    ),
                    expand=True
                )
            ),
        ],
        expand=True,
        tab_alignment=ft.TabAlignment.CENTER
    )
    page.add(
        ft.SafeArea(
            expand=True,
            content=tabs
        )
    )


ft.app(target=main, upload_dir="assets/uploads", view=ft.AppView.WEB_BROWSER, assets_dir="assets")