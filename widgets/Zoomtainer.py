import flet as ft
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

