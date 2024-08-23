import flet as ft



class BotonTexto(ft.Container):

    def handle_hover(self, e):
        if e.data == "true":
            self.bgcolor = ft.colors.ON_INVERSE_SURFACE
        else:
            self.bgcolor = ft.colors.BACKGROUND
        self.update()

    def click(self, e):
        if self.click_handler:
            self.click_handler(e)

    def __init__(
        self,
        texto="",
        ultimo=False,
        on_click=None,
    ):

        super().__init__()
        self.width = 100
        self.height = 50
        self.click_handler = on_click
        if not ultimo:
            self.border = ft.border.only(bottom=ft.border.BorderSide(width=1, color=ft.colors.ON_INVERSE_SURFACE))
        self.content = ft.Text(texto, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        self.on_click = self.click
        self.bgcolor = ft.colors.BACKGROUND
        self.on_hover = self.handle_hover
        self.alignment = ft.alignment.center