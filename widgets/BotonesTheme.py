import flet as ft
import random
class ColorButton(ft.IconButton):

    def change_color(self, e):
        random_color = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.page.theme.color_scheme_seed = "red"
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



if __name__ == "__main__":
    ft.app(target=ThemeButton)