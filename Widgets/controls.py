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


    def update_premio(self, e):
        # Aplicar el descuento del 15%
        self.sonido.play()
        if self.text_field_premio.value == '' or int(self.text_field_premio.value) <= 0:
            self.valor_final.value = "Ingresa un premio"
            self.boton_copiar.disabled = True
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

        self.sonido = ft.Audio(src="pop2.mp3")
        self.copy_sound = ft.Audio(src="bubble.mp3")

        self.sb_copiado = ft.SnackBar(
            content=ft.Text("Copiado al portapapeles"),
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
                
                ft.Row(
                    [
                        ft.Text("Premio con descuento: ", weight=ft.FontWeight.BOLD),
                        self.premio_display,
                    ],
                    expand=True
                ),
                self.boton_copiar
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

class ResponsiveControl(cv.Canvas):
    def __init__(self, content=None, resize_interval=10000, on_resize=None, expand=1, padding: ft.padding = 0, margin: ft.margin = 0, debug: str = False, **kwargs):
        super().__init__(**kwargs)
        self.content = ft.Container(
            content=content,
            padding=5 if debug else padding,
            alignment=ft.alignment.center,
            margin=5 if debug else margin,
            bgcolor=ft.colors.with_opacity(0.2, debug) if debug else None,
            border=ft.border.all(1, debug) if debug else None,
        )
        self.expand = expand
        self.resize_interval = resize_interval
        self.resize_callback = on_resize
        self.on_resize = self.__handle_canvas_resize
        self.size = namedtuple("size", ["width", "height"], defaults=[0, 0])

    def __handle_canvas_resize(self, e):
        """
        Called every resize_interval when the canvas is resized.
        If a resize_callback was given, it is called.
        """
        # print(e.data)
        pass

    def set_size(self):
        time.sleep(0.5)
        self.page.window.width = self.page.window.width + 1
        self.page.update()
        self.page.window.width = self.page.window.width - 1
        self.page.update()
        # print(f"Initial size after mount is [w={self.width}, h={self.height}]")

    def did_mount(self):
        self.page.run_thread(self.set_size)
        return super().did_mount()


class ResponsiveRow(ft.Row):
    def __init__(self, controls: list=[], expands: list=[], debug: str=False, expand: bool=True, **kwargs):
        super().__init__(**kwargs)
        self.expands = expands if expands else [1] * len(controls)
        self.controls = [
            ResponsiveControl(content=control, expand=self.expands[i], debug=debug)
            for i, control in enumerate(controls)
        ]
        self.expand = expand
        self.spacing = 0    

class ResponsiveColumn(ft.Column):
    def __init__(self, controls: list=[], expands: list=[], debug: str=False, expand: bool=True, **kwargs):
        super().__init__(**kwargs)
        self.expands = expands if expands else [1] * len(controls)
        self.controls = [
            ResponsiveControl(content=control, expand=self.expands[i], debug=debug)
            for i, control in enumerate(controls)
        ]
        self.expand = expand
        self.spacing = 0
class ChatBot(ft.Container):
    # we read the API key from env: genai_api_key
    def __init__(
            self,
            token,
            bot_name,
            user_name,
            json_path,
            tf_label = "Pregunta algo",
            auto_scroll=True,
            sleep=None,
            autofocus=False,
            autoload=False,
            bubble_radius=10,
            bubble_padding=5,
            animation_duration = 1000,
            user_header_bgcolor = ft.colors.PRIMARY_CONTAINER,
            user_header_border_color = ft.colors.PRIMARY,
            user_chat_bgcolor = ft.colors.PRIMARY_CONTAINER,
            user_chat_border_color = ft.colors.SECONDARY,
            bot_header_bgcolor = ft.colors.SECONDARY_CONTAINER,
            bot_header_border_color = ft.colors.PRIMARY,
            bot_chat_bgcolor = ft.colors.SECONDARY_CONTAINER,
            bot_chat_border_color = ft.colors.SECONDARY,
        ):
        super().__init__()
        genai.configure(api_key=token)
        self.bot_name = bot_name
        self.user_name = user_name
        self.json_path = json_path
        self.auto_scroll = auto_scroll
        self.sleep = sleep
        self.autofocus = autofocus
        self.bubble_radius = bubble_radius
        self.bubble_padding = bubble_padding
        self.autoload = autoload
        self.animation_duration = animation_duration
        self.tf_label = tf_label
        self.user_header_bgcolor = user_header_bgcolor
        self.user_header_border_color = user_header_border_color
        self.bot_header_bgcolor = bot_header_bgcolor
        self.bot_header_border_color = bot_header_border_color
        self.user_chat_bgcolor = user_chat_bgcolor
        self.user_chat_border_color = user_chat_border_color
        self.bot_chat_bgcolor = bot_chat_bgcolor
        self.bot_chat_border_color = bot_chat_border_color
        self.play_audio = False
        self.selected_image = None
        self.pil_image = None
        self.bot_message_container = None
        self.expand = True
        # self.on_click = self.disable_keyboard
                # Initialize COM for pyttsx3
        # pythoncom.CoInitialize()
        # self.engine = pyttsx3.init()
        # voices = self.engine.getProperty('voices')
        # for voice in voices:
        #     # print(voice)
        #     if "Helena" in voice.name:
        #     # if "Helena" in voice.name:  # Selecciona la voz de Zira
        #         self.engine.setProperty('voice', voice.id)
        #         # break
        # # self.engine.setProperty('voice', voices[1])
        # self.engine.setProperty('rate', 260)
        self.init_container()
        self.init_bot()
        try:
            self.load_history()
        except:
            pass

    def delete_image(self, e=None):
        self.selected_image = None
        self.pil_image = None
        self.button_adjuntar.icon_color = None
        self.button_adjuntar.on_click = self.pick_image
        self.button_adjuntar.update()

    def image_selected(self, e: ft.FilePickerResultEvent):
        # print(e.files[0].path)
        try:
            self.selected_image = e.files[0].path
            with open(e.files[0].path, "rb") as image_file:
                img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                # print(img_base64)
            img_data = base64.b64decode(img_base64)
            self.pil_image = PIL.Image.open(BytesIO(img_data))
            self.button_adjuntar.icon_color = "red"
            self.button_adjuntar.on_click = self.delete_image
            self.button_adjuntar.update()
        except Exception as e:
            pass

    def pick_image(self, e=None):
        self.image_uploader.pick_files(
            dialog_title="Elige una imagen",
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"],
            file_type=ft.FilePickerFileType.IMAGE,
        )

    def init_file_picker(self, page):
        self.image_uploader = ft.FilePicker(
            on_result=self.image_selected,
        )
        page.overlay.append(self.image_uploader)
        self.button_adjuntar.on_click = self.pick_image
        page.update()

    def did_mount(self):
        self.init_file_picker(self.page)
        # self.bot_audio = ft.Audio("asd")
        # self.page.overlay.append(self.bot_audio)
        return super().did_mount()
    
    def name_container(self, content, color, border_color, user):
        return ft.Container(
            padding=ft.padding.only(left=self.bubble_padding if user else 0, right=self.bubble_padding if not user else 0),
            content=ft.Container(
                content=content,
                bgcolor=color,
                border=ft.border.all(1, border_color),
                padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
                border_radius=ft.border_radius.only(
                    top_left=self.bubble_radius, bottom_left=0 if user else self.bubble_radius, top_right=self.bubble_radius, bottom_right=self.bubble_radius if user else 0
                ),
                # expand=True
            ),
        )
    def message_container(self, content, color, border_color, user, visible=True):
        return ft.Container(
            padding=ft.padding.only(left=self.bubble_padding if user else 0, right=self.bubble_padding if not user else 0),
            content=ft.Container(
                content=content,
                bgcolor=color,
                border=ft.border.all(1, border_color),
                padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
                border_radius=ft.border_radius.only(
                    top_left=self.bubble_radius if not user else 0, bottom_left=self.bubble_radius, top_right=0 if not user else self.bubble_radius, bottom_right=self.bubble_radius
                ),
                visible=visible
            ),
        )

    def disable_keyboard(self, e=None):
        self.tf_entrada.disabled = True
        self.tf_entrada.update()
        self.tf_entrada.disabled = False
        self.tf_entrada.update()

    def column_end(self):
        time.sleep(0.1)
        self.columna_principal.scroll_to(offset=-1, duration=0)

    def tf_submit(self, e):
        message = self.tf_entrada.value
        if not message:
            return
        
        self.tf_entrada.read_only = True
        self.tf_entrada.value = ""
        self.tf_entrada.update()

        user_name_container = self.name_container(
            ft.Text(f"{self.user_name}"),
            self.user_header_bgcolor,
            self.user_header_border_color,
            user=True)
        columna = ft.Column(
            [
                self.message_container(
                    ft.Markdown(
                        message,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        on_tap_link=lambda e: self.page.launch_url(e.data),
                        code_theme=ft.MarkdownCodeTheme.OCEAN,
                        expand=True,
                    ),
                    self.user_chat_bgcolor,
                    self.user_chat_border_color,
                    user=True
                )
            ],
            spacing=5
        )
        if self.selected_image:
            columna.controls.append(ft.Image(src=self.selected_image))
        user_message_container = ft.Container(
            expand=True,
            content=columna,
            animate_opacity=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            animate_offset=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            animate_scale=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            scale=0,
            opacity=0,
            offset=ft.Offset(-0.5,-0.5)
        )
        user_name_container.scale = 0
        user_name_container.opacity = 0
        user_name_container.offset = ft.Offset(-0.5,0.5)
        def show_user_name():
            time.sleep(0.1)
            user_message_container.scale = 1
            user_message_container.opacity = 1
            user_message_container.offset = ft.Offset(0,0)    
            user_message_container.update()
            user_name_container.scale = 1
            user_name_container.opacity = 1
            user_name_container.offset = ft.Offset(0,0)    
            user_name_container.update()
        user_name_container.animate_scale = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        user_name_container.animate_opacity = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        user_name_container.animate_offset = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        self.columna_principal.controls.append(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            user_name_container,
                            user_message_container
                        ],
                        spacing=0,
                        expand=True
                    )
                ],
                expand=True
            )
        )
        self.button_send.visible = False
        self.button_send.update()
        self.columna_principal.update()
        threading.Thread(target=self.column_end).start()
        threading.Thread(target=show_user_name).start()
        self.send_message(message)
        self.delete_image()
        self.save_history()
        self.tf_entrada.read_only = False
        self.tf_entrada.update()
        self.columna_principal.update()
        if self.autofocus:
            self.tf_entrada.focus()
        threading.Thread(target=self.column_end).start()
        self.update()

    def tf_change(self, e):
        if self.tf_entrada.value:
            self.button_send.visible = True
            self.button_send.update()
        else:
            self.button_send.visible = False
            self.button_send.update()

    def toggle_options(self, e):
        if self.row_opciones.visible:
            self.row_opciones.scale = 0
            self.row_opciones.update()
            time.sleep(self.animation_duration/8000)
            self.row_opciones.visible = False
            self.button_expandir_opciones.icon = ft.icons.ARROW_LEFT_SHARP
        else:
            self.row_opciones.visible = True
            self.row_opciones.update()
            time.sleep(self.animation_duration/8000)
            self.row_opciones.scale = 1
            self.button_expandir_opciones.icon = ft.icons.ARROW_RIGHT_SHARP
        self.button_expandir_opciones.update()
        self.row_opciones.update()

    def init_container(self):
        self.tf_entrada = ft.TextField(
            label=self.tf_label,
            autofocus=True,
            on_submit=self.tf_submit,
            expand=True,
            on_change=self.tf_change,
            content_padding=5,
            height=40,
            multiline=True
        )
        self.columna_principal = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            auto_scroll=self.auto_scroll,
            spacing=5,
        )
        self.button_send = ft.IconButton(
            ft.icons.SEND,
            on_click=self.tf_submit,
            visible=False
        )

        self.button_adjuntar = ft.IconButton(
            ft.icons.UPLOAD_SHARP,

        )
        self.button_expandir_opciones = ft.IconButton(
            ft.icons.ARROW_LEFT_SHARP,
            on_click=lambda e: threading.Thread(target=self.toggle_options(e)).start(),
            visible=True
        )
        self.row_opciones = ft.Row(
            controls=[
                self.button_adjuntar
            ],
            scale=0,
            animate_scale=ft.Animation(int(self.animation_duration/8), ft.AnimationCurve.EASE_IN_OUT),
            visible=False,
        )
        self.buttons_row = ft.Row(
            [
                self.row_opciones,
                self.button_expandir_opciones,
                self.button_send,
            ],
            spacing=0
        )
        self.content_chat = ft.Column(
            controls=[
                self.columna_principal,
                ft.Row(
                    controls=[
                        ft.Row(
                            [
                                self.tf_entrada,
                                self.buttons_row
                            ],
                            expand=True,
                            spacing=0
                        )
                    ],
                    # expand=True
                ),
            ],
            expand=True
        )
        self.content = ft.SafeArea(
            expand=True,
            content=self.content_chat
            # ResponsiveColumn(
            #     controls=[
            #         ResponsiveControl(
            #             ,
            #             # debug="red"
            #         )
            #     ]
            # )
        )
        
        


    def init_bot(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])
        self.response = None
        if self.autoload:
            self.load_history()

    def show_response(self):
        self.bot_message_container.visible = True
        self.bot_message_container.update()
        time.sleep(0.15)
        self.bot_message_container.scale = 1
        self.bot_message_container.opacity = 1
        self.bot_message_container.offset = ft.Offset(0,0)    
        self.bot_message_container.update()

    def send_message(self, message):
        contenido = [message]
        if self.pil_image:
            contenido[0] = "Analyze the provided image thoroughly and generate an exhaustive, meticulous description capturing every detail with pinpoint accuracy. ; prioritize thoroughness and precision over conciseness.. ((RESPONDE EN UN SOLO PARRAFO NO MAS DE 250 PALABRAS))"
            contenido.append(self.pil_image)
        self.md_response = ft.Markdown(
            "",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: self.page.launch_url(e.data),
            code_theme=ft.MarkdownCodeTheme.OCEAN,
            expand=True,
        )
        self.bot_message_container = ft.Container(
            self.message_container(
                self.md_response,
                self.bot_chat_bgcolor,
                self.bot_chat_border_color,
                user=False,
            ),
            animate_opacity=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            animate_offset=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            animate_scale=ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN),
            scale=0,
            opacity=0,
            offset=ft.Offset(0.5,0.5),
            expand=True,
            visible=False
        )
        bot_name_container = self.name_container(
            ft.Text(f"{self.bot_name}"),
            self.bot_header_bgcolor,
            self.bot_header_border_color,
            user=False
        )
        bot_name_container.scale = 0
        bot_name_container.opacity = 0
        bot_name_container.offset = ft.Offset(0.5,0.5)
        def show_user_name():
            time.sleep(0.15)
            bot_name_container.scale = 1
            bot_name_container.opacity = 1
            bot_name_container.offset = ft.Offset(0,0)    
            bot_name_container.update()
        bot_name_container.animate_scale = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        bot_name_container.animate_opacity = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        bot_name_container.animate_offset = ft.Animation(self.animation_duration, ft.AnimationCurve.FAST_OUT_SLOWIN)
        self.columna_principal.controls.append(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row(
                                expand=True,
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    bot_name_container,
                                ]
                            ),
                            ft.Row(
                                expand=True,
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    self.bot_message_container,
                                ]
                            )
                        ],
                        spacing=0,
                        expand=True
                    )
                ],
                expand=True
            )
        )
        self.columna_principal.update()
        
        def update_message():
            def get_response():
                try:
                    self.response = self.chat.send_message(
                        content=contenido,
                        safety_settings={
                            'HARASSMENT': 'block_none',
                            'SEXUALLY_EXPLICIT': 'block_none',
                            'HATE_SPEECH': 'block_none',
                        },
                        stream=True
                    )
                except:
                    print("error al response")
            while not self.response:
                get_response()
                time.sleep(0.5)
            for chunk in self.response:
                time.sleep(0.5)
                if not self.bot_message_container.visible:
                    # print("funciona")
                    # self.show_response()
                    threading.Thread(target=self.show_response).start()
                try:
                    for letter in chunk.text:
                        # print(letter)
                        self.md_response.value += letter # chunk.text
                        self.md_response.update()
                except Exception as e:
                    last_send, last_received = self.chat.rewind()
                    print("puto error")
                    # self.md_response.value = self.response.text # chunk.text
                    # self.md_response.update()
                    # self.send_message(message)
                self.columna_principal.scroll_to(offset=0, curve=ft.AnimationCurve.FAST_OUT_SLOWIN, duration=100)
            
        def save_then_play():
            if os.path.exists("bot.mp3"):
                os.remove("bot.mp3")
            # self.engine.save_to_file(self.md_response.value, "bot.mp3")
            # self.engine.runAndWait()
            # self.engine.stop()
            # self.bot_audio.pause()
            # self.page.overlay.remove(self.bot_audio)
            # self.bot_audio = ft.Audio(src="bot.mp3")
            # self.page.overlay.append(self.bot_audio)
            self.page.update()
            time.sleep(0.5)
            # if self.play_audio:
                # self.bot_audio.play()
        show_user_name()
        update_message()
        # threading.Thread(target=show_user_name).start()
        # threading.Thread(target=update_message).start()
        threading.Thread(target=save_then_play).start()

    def get_candidate(self):
        return self.response.candidates

    def get_models(self):
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                pass
                # print(m.name)

    def reset_history(self):
        self.chat = self.model.start_chat(history=[])
        self.save_history

    def load_history(self):
        try:
            with open(self.json_path, 'r') as f:
                chat_history = json.load(f)
        except FileNotFoundError:
            chat_history = []

        if not chat_history:
            return

        for message in chat_history:
            role = message['role']
            text = message['text']
            
            # Convertir el formato al que espera el modelo
            if role == 'user':
                self.chat.history.append({
                    'role': 'user',
                    'parts': [{'text': text}]
                })
            elif role == 'model':
                self.chat.history.append({
                    'role': 'model',
                    'parts': [{'text': text}]
                })

    def save_history(self):
        chat_history_serializable = []
        for message in self.chat.history:
            # Verificar si el mensaje es un objeto Content
            if hasattr(message, 'role') and hasattr(message, 'parts'):
                role = message.role
                # Asumimos que el texto está en la primera parte del mensaje
                text = message.parts[0].text if message.parts else ""
            else:
                # Si no es un objeto Content, intentamos acceder como diccionario
                role = message.get('role', 'unknown')
                text = message.get('parts', [{}])[0].get('text', "")

            chat_history_serializable.append({
                'role': role,
                'text': text
            })

        with open(self.json_path, 'w') as f:
            json.dump(chat_history_serializable, f, indent=4)
