import flet as ft
from Widgets.controls import *
from Widgets.funcs import *
class NavigationApp:

    def cambiar_destino(self, e: ft.OptionalEventCallable):
        self.animation_switcher.content = self.pages[int(e.data)]
        self.animation_switcher.update()

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
        self.pages = [
            ft.Column(
                expand=True,
                controls=page,
            )
            for page in pages
        ]
        self.columna_main = self.pages[0]
        self.animation_switcher = ft.AnimatedSwitcher(
            ft.Container(expand=True, content=self.columna_main),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=100,
            reverse_duration=10,
        )
        self.page.add(ft.SafeArea(
            expand=True,
            content=self.animation_switcher
        ))
        self.page.update()



def main(page: ft.Page):
    page.fonts = {
        "GasoekOne": github_to_raw("https://github.com/chrisbull/font-collection/blob/master/Dank%20Mono/DankMono-Regular.ttf")
    }

    page.theme = ft.Theme(font_family="GasoekOne")
    page.title = "Utilidades Oficina"
    page.theme_mode = ft.ThemeMode.LIGHT
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
            [
                ft.Container(content=ft.Tabs(
                    [
                        TabFederacionFranquicias(),
                    ],
                    tab_alignment=ft.TabAlignment.CENTER,
                    expand=True
                ))
            ],
            [
                ft.Container(content=ft.Tabs(
                    [
                        TabGeneralPatentes(),
                    ],
                    tab_alignment=ft.TabAlignment.CENTER,
                    expand=True
                ))
            ],
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
                                    font_family="GasoekOne"
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
            ft.NavigationBarDestination(icon=ft.icons.MENU, label="FED"),
            ft.NavigationBarDestination(icon=ft.icons.MENU, label="GENERAL"),
            # ft.NavigationBarDestination(icon=ft.icons.MENU, label="123"),
            ft.NavigationBarDestination(icon=ft.icons.MENU, label="CHATBOT"),
        ],
    )

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
