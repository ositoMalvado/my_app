import flet as ft
import math



class CalculadoraPremio(ft.Container):


    def update_premio(self, e):
        # Aplicar el descuento del 15%
        self.sonido.play()
        if self.text_field_premio.value == '':
            self.valor_final.value = "0"
            self.valor_final.update()
            if e.control.data == "descuento":
                return
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
        print(self.copy_value)
        self.premio_display.value = "$" + str(int(final_value))
        self.premio_display.update()
        self.valor_final.value = str(int(self.cuotas)) + " cuotas de " + str(int(final_value/self.cuotas))
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
        self.sb_copiado.open = True
        self.page.update()

    def did_mount(self):
        self.page.overlay.append(self.sb_copiado)
        self.page.overlay.append(self.sonido)
        self.page.overlay.append(self.copy_sound)
        self.page.update()
        return super().did_mount()

    def __init__(self):
        super().__init__()

        self.sonido = ft.Audio(src="bamboo.mp3")
        self.copy_sound = ft.Audio(src="copy.mp3")

        self.sb_copiado = ft.SnackBar(
            content=ft.Text("Copiado al portapapeles"),
            bgcolor=ft.colors.GREEN
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

        self.valor_final = ft.Text("0", expand=True, text_align=ft.TextAlign.CENTER)

        self.text_field_premio = ft.TextField(
            label="Premio",
            prefix_icon=ft.icons.ATTACH_MONEY_ROUNDED,
            hint_text="Ingresa el premio",
            # height=100,
            content_padding=ft.padding.all(5),
            on_change=self.update_premio,
            input_filter = ft.InputFilter(
                regex_string=r"[1-9][0-9]*",
                allow=True,
                replacement_string="",
            )
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
        )

        self.descuento_display = ft.Text(str(self.descuento) + "%", weight=ft.FontWeight.BOLD)

        self.intervalo = 300
        self.intervalo_slider = ft.Slider(
            value=self.intervalo,
            min=0,
            max=1000,
            divisions=20, # i need each division be by 50
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
                ft.Text("Calculadora de Premio", weight=ft.FontWeight.BOLD),
                self.text_field_premio,
                ft.Row(
                    [
                        ft.Text("Descuento: ", weight=ft.FontWeight.BOLD),
                        self.descuento_display,
                    ]
                ),
                self.slider,
                ft.Row(
                    [
                        ft.Text("Intervalo: ", weight=ft.FontWeight.BOLD),
                        self.intervalo_display,
                    ]
                ),
                self.intervalo_slider,
                ft.Row(
                    [
                        ft.Text("Cuotas: ", weight=ft.FontWeight.BOLD),
                        self.cuotas_display,
                    ]
                ),
                self.cuotas_slider,
                
                ft.Row(
                    [
                        ft.Text("Premio con descuento: ", weight=ft.FontWeight.BOLD),
                        self.premio_display,
                    ]
                ),
                self.boton_copiar
            ],
            spacing=2,
        )
        self.border_radius=10
        self.border=ft.border.all(1, ft.colors.BLACK12)
        self.bgcolor=ft.colors.PRIMARY_CONTAINER
        self.width=500
        self.padding=10

