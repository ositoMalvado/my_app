import asyncio
import flet as ft
from Widgets.controls import *

class NavigationApp:

    def cambiar_destino(self, e: ft.OptionalEventCallable):
        self.page.controls = self.pages[int(e.data)]
        self.page.update()

    def __init__(self,
            page: ft.Page,
            pages: list[ft.Control],
            destinations: list[ft.NavigationDestination]):
        self.page = page
        self.destinations = destinations
        self.page.navigation_bar = ft.NavigationBar(
            destinations=self.destinations,
            on_change=self.cambiar_destino,
        )
        self.pages = pages

        self.page.controls = self.pages[0]
        self.page.update()



def main(page: ft.Page):
    page.bgcolor = ft.colors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme(
        color_scheme_seed="#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )
    page.update()
    app = NavigationApp(
        page,
        pages=[
            [
                ft.Container(content=CalculadoraPremio())
            ],
            # [
            #     ft.Container(content=ft.Text("FED"))
            # ],
            # [
            #     ft.Container(content=ft.Text("123"))
            # ],
            [
                ft.Container(content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ThemeButton(),
                                ColorButton(),
                            ],
                        ),
                        ft.Column(
                            [
                                ChatBot(
                                    token="AIzaSyCTpmY_rKZLlWc-AnnyjUqbj5SHrfG3NWo",
                                    bot_name=f"ChatBot",
                                    user_name="Usuario",
                                    json_path=f"chat_history.json",
                                    autofocus=False,
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True
                ),
                expand=True)
            ],
        ],
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.MENU, label="RUS"),
            # ft.NavigationBarDestination(icon=ft.icons.MENU, label="FED"),
            # ft.NavigationBarDestination(icon=ft.icons.MENU, label="123"),
            ft.NavigationBarDestination(icon=ft.icons.MENU, label="XCV"),
        ],
    )

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)