import flet as ft
from widgets.BotonTexto import BotonTexto
from widgets.BotonesTheme import *

def main(page: ft.Page):

    titulo = "Utilidades"


    page.padding = 0
    page.spacing = 0



    def menu_click(e):
        if container_menu.offset == ft.Offset(0, 0):
            container_menu.offset = ft.Offset(-1, 0)
            container_menu.opacity = 0
            menu_button.icon = ft.icons.MENU
        else:
            container_menu.offset = ft.Offset(0, 0)
            container_menu.opacity = 1
            menu_button.icon = ft.icons.ARROW_BACK_ROUNDED
        menu_button.update()
        container_menu.update()

    menu_button = ft.IconButton(
        ft.icons.MENU,
        on_click=menu_click
    )


    app_bar = ft.AppBar(
        leading=menu_button,
        title=ft.Text(titulo),
        center_title=True
    )

    page.appbar = app_bar

    app_stack = ft.Stack(
        controls=[],
        expand=True
    )


    columna_principal = ft.Column(
        [
            ft.Text("hola principal")
        ],
        # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )


    container_principal = ft.Container(
        content=columna_principal,
        expand=True
    )

    def agregar_texto(e):

        columna_principal.controls.append(
            ft.Text(f"texto {len(columna_principal.controls)}")
        )
        columna_principal.update()

    menu_items = [
        ft.Row([ThemeButton(), ColorButton()]),
        BotonTexto(texto=f"Inicio", on_click=agregar_texto),
        BotonTexto(texto=f"Federación Patronal", on_click=agregar_texto),
        BotonTexto(texto=f"Río Uruguay", on_click=agregar_texto),
        BotonTexto(texto=f"General", on_click=agregar_texto, ultimo=True),
        
    ]

    columna_menu = ft.Column(
        menu_items,
        spacing=0,
        scroll="auto",
        expand=True
    )

    container_menu = ft.Container(
        content=columna_menu,
        expand=True,
        offset=ft.Offset(-1, 0),
        opacity=0,
        animate_opacity=ft.Animation(333, ft.AnimationCurve.EASE_IN_OUT),
        border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.ON_INVERSE_SURFACE)),
        bgcolor=ft.colors.BACKGROUND,
        padding=ft.padding.only(left=10, right=10),
        animate_offset=ft.Animation(333, ft.AnimationCurve.EASE_IN_OUT)
    )

    app_stack.controls.append(container_principal)
    app_stack.controls.append(container_menu)

    page.add(
        ft.SafeArea(
            app_stack,
            expand=True
        )
    )


ft.app(main)
