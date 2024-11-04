import time
import flet as ft
from components.functions import *
from components.widgets import *
import os
import shutil
import socket
from typing import Dict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import json
import webbrowser
from functools import partial
import google.generativeai as genai
import PIL.Image

os.environ["FLET_SECRET_KEY"] = "zxczxczxcSS"
os.environ["FLET_UPLOAD_DIR"] = "assets/uploads"
os.environ["FLET_ASSETS_DIR"] = "assets"
assets_dir = "assets"
upload_dir = os.path.join(assets_dir, "uploads")

# Ensure upload directory exists
os.makedirs(upload_dir, exist_ok=True)




def get_local_ip():
    try:
        # Crear un socket UDP para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"  # Fallback a todas las interfaces si no se puede determinar la IP



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
            font_family=None,
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
        self.font_family = font_family
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
                        code_style_sheet=ft.TextStyle(font_family=self.font_family) if self.font_family else None,
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
        
        def close_keyboard(e):
            print("funciona")
            self.tf_entrada.disabled = True
            self.tf_entrada.update()
            time.sleep(0.01)
            self.tf_entrada.disabled = False
            self.tf_entrada.update()
        self.tf_entrada = ft.TextField(
            label=self.tf_label,
            autofocus=True,
            on_submit=self.tf_submit,
            expand=True,
            on_change=self.tf_change,
            suffix=ft.IconButton(
                ft.icons.KEYBOARD_ARROW_DOWN,
                on_click=close_keyboard,
                padding=0,
                height=40,
            ),
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


    def will_unmount(self):
        print("desmontado")
        self.working = False
        return super().will_unmount()

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
            code_style_sheet=ft.TextStyle(font_family=self.font_family) if self.font_family else None,
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
                    self.working = True
                    self.finalizado = False
                    for letter in chunk.text:
                        # print(letter)
                        if self.working and not self.finalizado:
                            self.md_response.value += letter # chunk.text
                            self.md_response.update()
                except Exception as e:
                    try:
                        last_send, last_received = self.chat.rewind()
                    except:
                        try:
                            self.response.resolve()
                        except:
                            print("puto error 0 de 2")
                        print("puto error 1 de 2")
                    print("puto error 2 de 2")
                    # self.md_response.value = self.response.text # chunk.text
                    # self.md_response.update()
                    # self.send_message(message)
                if self.working:
                    self.columna_principal.scroll_to(offset=0, curve=ft.AnimationCurve.FAST_OUT_SLOWIN, duration=100)
            self.response = None
            self.working = False
            self.finalizado = False
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




class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.generate_html().encode())
        else:
            # Manejar el error de favicon.ico
            if self.path == '/favicon.ico':
                self.send_response(404)
                self.end_headers()
                return
            super().do_GET()

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except BrokenPipeError:
            # Ignorar errores de pipe roto
            pass
    def generate_html(self):
        files = os.listdir(upload_dir)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Servidor July</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
            <style>
                :root {{
                    --primary: #4CAF50;
                    --primary-dark: #45a049;
                    --glass-bg: rgba(255, 255, 255, 0.1);
                    --glass-border: rgba(255, 255, 255, 0.2);
                }}

                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}

                body {{
                    min-height: 100vh;
                    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                    background-size: 400% 400%;
                    animation: gradient 15s ease infinite;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    padding: 20px;
                    color: white;
                    overflow-x: hidden;
                }}

                @keyframes gradient {{
                    0% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0% 50%; }}
                }}

                .container {{
                    max-width: 1000px;
                    width: 100%;
                    background: var(--glass-bg);
                    backdrop-filter: blur(12px);
                    border: 1px solid var(--glass-border);
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    margin-top: 20px;
                    transition: transform 0.3s ease;
                }}

                .table-container {{
                    max-height: 70vh;
                    overflow-y: auto;
                    border-radius: 15px;
                    padding-right: 5px;
                }}

                .table-container::-webkit-scrollbar {{
                    width: 8px;
                }}

                .table-container::-webkit-scrollbar-track {{
                    background: var(--glass-bg);
                    border-radius: 10px;
                }}

                .table-container::-webkit-scrollbar-thumb {{
                    background: var(--glass-border);
                    border-radius: 10px;
                }}

                h1 {{
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 30px;
                    background: linear-gradient(to right, #fff, #a5f3fc);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    position: relative;
                    animation: title-glow 2s ease-in-out infinite;
                }}

                @keyframes title-glow {{
                    0%, 100% {{ text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }}
                    50% {{ text-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }}
                }}

                table {{
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0 8px;
                }}

                tr {{
                    transition: all 0.2s ease;
                    opacity: 0;
                    transform: translateY(10px);
                }}

                tr:hover {{
                    transform: translateX(5px) !important;
                }}

                th, td {{
                    padding: 15px;
                    text-align: left;
                    background: var(--glass-bg);
                    border: 1px solid var(--glass-border);
                }}

                th {{
                    position: sticky;
                    top: 0;
                    background: rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(12px);
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    z-index: 10;
                }}

                td:first-child, th:first-child {{
                    border-radius: 10px 0 0 10px;
                }}

                td:last-child, th:last-child {{
                    border-radius: 0 10px 10px 0;
                }}

                .download-btn {{
                    color: #fff;
                    background: linear-gradient(135deg, #00f260, #0575e6);
                    border: none;
                    padding: 10px 20px;
                    border-radius: 30px;
                    text-decoration: none;
                    display: inline-block;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }}

                .download-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                }}

                .empty-message {{
                    text-align: center;
                    padding: 40px;
                    font-size: 1.2em;
                    background: var(--glass-bg);
                    border-radius: 15px;
                    border: 1px solid var(--glass-border);
                    animation: message-pulse 2s infinite;
                }}

                @keyframes message-pulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                    100% {{ transform: scale(1); }}
                }}

                .particles {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: -1;
                    opacity: 0.5;
                }}
            </style>
        </head>
        <body>
            <div class="particles" id="particles"></div>
            <div class="container">
                <h1>Servidor Archivos (july 🐎)</h1>
                {"<p class='empty-message'>No hay archivos disponibles para descargar.</p>" if not files else f'''
                <div class="table-container">
                    <table>
                        <tr>
                            <th>Nombre del archivo</th>
                            <th>Acciones</th>
                        </tr>
                        {"".join([self.generate_file_row(file) for file in files])}
                    </table>
                </div>
                '''}
            </div>

            <script>
                function createParticles() {{
                    const particlesContainer = document.getElementById('particles');
                    const particleCount = 30; // Reduced particle count
                    
                    for (let i = 0; i < particleCount; i++) {{
                        const particle = document.createElement('div');
                        particle.className = 'particle';
                        particle.style.width = '3px';
                        particle.style.height = '3px';
                        particle.style.background = 'rgba(255, 255, 255, 0.5)';
                        particle.style.borderRadius = '50%';
                        particle.style.position = 'absolute';
                        particle.style.left = `${{Math.random() * 100}}vw`;
                        particle.style.top = `${{Math.random() * 100}}vh`;
                        
                        particlesContainer.appendChild(particle);
                        
                        animateParticle(particle);
                    }}
                }}

                function animateParticle(particle) {{
                    const duration = 10 + Math.random() * 20;
                    const startX = parseFloat(particle.style.left);
                    const startY = parseFloat(particle.style.top);
                    
                    gsap.to(particle, {{
                        duration: duration,
                        x: -20 + Math.random() * 40,
                        y: -20 + Math.random() * 40,
                        opacity: gsap.utils.random(0.3, 0.7),
                        ease: "none",
                        repeat: -1,
                        yoyo: true
                    }});
                }}

                function handleHover() {{
                    const container = document.querySelector('.container');
                    
                    container.addEventListener('mousemove', (e) => {{
                        const rect = container.getBoundingClientRect();
                        const x = (e.clientX - rect.left) / rect.width - 0.5;
                        const y = (e.clientY - rect.top) / rect.height - 0.5;
                        
                        gsap.to(container, {{
                            duration: 0.5,
                            rotationY: x * 5, // Reduced rotation
                            rotationX: -y * 5, // Reduced rotation
                            ease: "power2.out"
                        }});
                    }});
                    
                    container.addEventListener('mouseleave', () => {{
                        gsap.to(container, {{
                            duration: 0.5,
                            rotationY: 0,
                            rotationX: 0,
                            ease: "power2.out"
                        }});
                    }});
                }}

                document.addEventListener('DOMContentLoaded', () => {{
                    createParticles();
                    handleHover();
                    
                    // Animate table rows
                    const rows = document.querySelectorAll('tr');
                    gsap.to(rows, {{
                        opacity: 1,
                        y: 0,
                        duration: 0.5,
                        stagger: 0.05,
                        ease: "power2.out"
                    }});
                }});
            </script>
        </body>
        </html>
        """
        return html_content

    def generate_file_row(self, filename):
        return f"""
        <tr>
            <td>{filename}</td>
            <td><a href="/uploads/{filename}" download class="download-btn">Descargar</a></td>
        </tr>
        """

class FileUploader(ft.Container):
    def __init__(
        self,
        ring_size:int = 20,
        server_port:int = 8000
    ):
        super().__init__()

        self.server_port = server_port
        self.server = None
        self.server_thread = None
        self.is_server_running = False
        self.local_ip = get_local_ip()

        self.ring_size = ring_size
        self.icon_size = self.ring_size * 0.75
        self.progs_ring: Dict[str, ft.ProgressBar] = {}
        self.anim_switchers: Dict[str, ft.AnimatedSwitcher] = {}
        self.files_column = ft.Column()
        
        self.fp = ft.FilePicker(
            on_result=self.handle_file_picked
        )

        self.upload_button = ft.ElevatedButton("Subir", on_click=self.handle_upload, visible=False)
        
        # Server controls con IP local
        self.server_status = ft.Text("Apagado", color="red")
        self.ip_text = ft.Text(f"IP: {self.local_ip}", visible=False)
        self.server_button = ft.ElevatedButton(
            "Encender",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.toggle_server,
            bgcolor=ft.colors.GREEN
        )
        
        self.server_url = ft.TextButton(
            "Abrir en el navegador",
            icon=ft.icons.OPEN_IN_BROWSER,
            on_click=lambda _: webbrowser.open(f"http://{self.local_ip}:{self.server_port}"),
            visible=False
        )

        self.content = ft.Column(
            [
                ft.ElevatedButton(
                    "Seleccionar archivos",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: self.fp.pick_files(
                        allow_multiple=True,
                        allowed_extensions=["jpg", "png", "jpeg", "pdf", "mp4", "mp3", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "bat", "sh", "py", "c", "cpp", "java", "css", "js", "html", "php", "rb", "go", "js", "py", "cs", "json", "xml", "svg", "psd", "ai", "eps", "indd", "ps", "pdf"]
                    ),
                ),
                self.server_button,
                ft.Row(
                    [
                        self.server_status,
                        self.ip_text,
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                self.server_url,
                self.upload_button,
                self.files_column
            ]
        )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return
        
        # first of all we remove evry file from assets/uploads
        for f in os.listdir(upload_dir):
            os.remove(os.path.join(upload_dir, f))
        
        
        self.upload_button.visible = True
        self.upload_button.update()
        self.progs_ring = {}
        self.anim_switchers = {}
        self.files_column.controls.clear()
        
        for f in e.files:
            progress_ring = ft.ProgressRing(
                value=0,
                width=self.ring_size,
                height=self.ring_size,
                color=ft.colors.GREEN
            )
            
            switcher = ft.AnimatedSwitcher(
                content=ft.Container(
                    width=self.ring_size,
                    height=self.ring_size,
                    content=ft.Icon(
                        ft.icons.UPLOAD_FILE,
                        expand=True,
                        size=self.icon_size
                    ),
                ),
                duration=300,
                reverse_duration=100,
                transition=ft.AnimatedSwitcherTransition.SCALE
            )
            
            self.progs_ring[f.name] = progress_ring
            self.anim_switchers[f.name] = switcher
            
            self.files_column.controls.append(
                ft.Row(
                    [
                        ft.Stack([progress_ring, switcher]),
                        ft.Text(f.name),
                    ]
                )
            )
        self.update()

    def handle_upload(self, e):
        if self.fp.result and self.fp.result.files:
            for f in self.fp.result.files:
                try:
                    dest_path = os.path.join(upload_dir, f.name)
                    shutil.copy2(f.path, dest_path)
                    
                    self.progs_ring[f.name].value = 100
                    self.anim_switchers[f.name].content = ft.Container(
                        width=self.ring_size,
                        height=self.ring_size,
                        content=ft.Icon(
                            ft.icons.DONE,
                            expand=True,
                            size=self.icon_size
                        ),
                    )
                except Exception as ex:
                    print(f"Error subiendo {f.name}: {str(ex)}")
                    self.progs_ring[f.name].color = ft.colors.RED
                    self.anim_switchers[f.name].content = ft.Container(
                        width=self.ring_size,
                        height=self.ring_size,
                        content=ft.Icon(
                            ft.icons.ERROR,
                            expand=True,
                            size=self.icon_size
                        ),
                    )
                finally:
                    self.progs_ring[f.name].update()
                    self.anim_switchers[f.name].update()

    def start_server(self):
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        handler = partial(CustomHandler, directory=assets_dir)
        # Cambiar 'localhost' por '0.0.0.0' para escuchar en todas las interfaces
        self.server = ThreadingHTTPServer(('0.0.0.0', self.server_port), handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.is_server_running = True
        
        self.server_status.value = f"Server: Running on port {self.server_port}"
        self.server_status.color = "green"
        self.server_button.text = "Stop Server"
        self.server_button.icon = ft.icons.STOP
        self.server_button.bgcolor = ft.colors.RED
        self.server_url.visible = True
        self.ip_text.visible = True
        self.update()

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_server_running = False
            
            self.server_status.value = "Apagado"
            self.server_status.color = "red"
            self.server_button.text = "Encender"
            self.server_button.icon = ft.icons.PLAY_ARROW
            self.server_button.bgcolor = ft.colors.GREEN
            self.server_url.visible = False
            self.ip_text.visible = False
            
            self.update()

    def toggle_server(self, e):
        if self.is_server_running:
            self.stop_server()
        else:
            self.start_server()

    def did_mount(self):
        self.page.overlay.append(self.fp)
        self.page.update()
        return super().did_mount()

    def will_unmount(self):
        self.stop_server()
        return super().did_mount()


class RusContactos(ft.Tabs):
    telefonos_titulos = {
        "Casa Central": [
            {
                "Oficina": "2994479915",
                "Oficina2": "2994479957",
                "Oficina3": "2994479980",
            }
        ],
        "Comercial": [
            {
                "Flavia": "2994632023",
                "Juliana": "2995011208",
            }
        ],
        "Siniestros": [
            {
                "Jorge": "2994632027",
                "Nicolas": "2995065042",
            }
        ],
        "FastTrack": [
            {
                "Natalia": "2995020709",
                "Cynthia": "2995030342",
                "Daniela": "2995030364",
            }
        ],
        "General": [
            {
                "RUS1": "1120401133",
                "RUS2": "1120401236",
            }
        ],
        "Soporte Agencia Digital": [
            {
                "Cobranzas": "1151686028",
                "Siniestros": "1120401133",
                "Producción": "1120401236",
            }
        ],
        "Emergencias": [
            {
                "Atención al asegurado": "08008887787",
                "Auxilio mecánico": "08004441441",
                "Desde el exterior": "3514858321",
            }
        ],
        "Contrataciones": [
            {
                "Contrataciones": "2995011208",
            }
        ],
    }

    correos_data = {
        "Vehículos": {
            "TOTALES": {
                "Descripción": "Este equipo gestionará integralmente el 100% de los siniestros de Robo Total, Daños Total e Incendio Total Bolsa CRM: Siniestros Automotores - Totales",
                "Correo": ["siniestrostotales@riouruguay.com.ar"],
            },
            "DAÑOS PARCIALES": {
                "Descripción": "Este equipo gestionará los casos de, Daños Parciales de Todo Riesgo, Robos, Parciales (no ruedas y baterías), Daños, de Granizo e Incendio Parcial.",
                "Correo": ["siniestrosparciales@riouruguay.com.ar"],
            },
            "FAST TRACKAUTOMOTORES": {
                "Descripción": "Este equipo gestionará reclamos de Daños de Cristales, Cerraduras y Robo de Ruedas y Batería. Bolsa CRM: Siniestros Automotores - Fast Track",
                "Correo": ["siniestrosparcialesft@riouruguay.com.ar"],
            },
        },
        "CLEAS": {
            "TRAMITACIONES": {
                "Descripción": "Este equipo definira la responsabilidad del 100% de casos ue ingresen a la plataforma CLEAS. Bolsa CRM: Siniestros Automotores - Cleas - Tramitación",
                "Correo": ["siniestroscleas@riouruguay.com.ar"],
            },
            "CIERRES": {
                "Descripción": "Este equipo definira la responsabilidad del 100% de casos CLEAS y gestionará los cierres de aquellos trámites definidos a favor de RUS donde la antguedad de los vehículos sea mayor a 15 años. Bolsa CRM: Siniestros Automotores - Cleas - Cierres",
                "Correo": ["siniestroscleasgestion@riouruguay.com.ar"],
            },
        },
        "Responsabilidad Civil": {
            "RC DAÑOS MATERIALES": {
                "Descripción": "Este equipo gestionará los Reclamos de RC únicamente por Daños Materiales de todo el tamaño y que ingresen por todos los canales de comunicación. Bolsa CRM: Siniestros Terceros - Daños Materiales",
                "Correo": ["reclamosmateriales@riouruguay.com.ar"],
            },
            "RC LESIONADOS y FALLECIDOS": {
                "Descripción": "Este equipo gestionará los Reclamos de RC con Terceros Lesionados y/o Fallecidos, de todo el país y que ingresen por todos los canales de comunicación. Bolsa CRM: Siniestros Terceros - Lesiones",
                "Correo": ["lesiones@riouruguay.com.ar"],
            },
            "MEDIACIONES": {
                "Descripción": "Este equipo gestionará los Reclamos que pasan a la Instancia de Mediación Judicial, de todos los Ramos y de todo el país. Bolsa CRM: Siniestros Terceros- Mediaciones",
                "Correo": ["mediaciones@riouruquay.com.ar"],
            },
        },
        "Otros": {
            "SINIESTROS EN EL EXTERIOR": {
                "Descripción": "Este equipo gestionará los siniestros, de Asegurados y Terceros, ocurridos en países limítrofes. Bolsa CRM: Siniestros Terceros - En el Exterior",
                "Correo": ["siniestrosexterior@riouruguay.com.ar"],
            },
            "RIESGOS ESPECIALES VARIAS": {
                "Descripción": "Este equipo gestionará siniestros de Riesgos Agrícolas y Caución. Bolsa CRM: Siniestros Varias - Riesgos Especiales",
                "Correo": [
                    "siniestrosgranizo@riouruguay.com.ar",
                    "siniestroscaucion@riouruguay.com.ar",
                ],
            },
            "PATRIMONIALES VARIAS": {
                "Descripción": "Este equipo gestionará siniestros de Riesgos Patrimoniales (Lo que no es fast track). Los ramos que incluye son Hogar y Comercio con sus coberturas de Robo, Daños por agua y Incendio. Bolsa CRM: Siniestros Patrimoniales - Varias",
                "Correo": ["siniestrospatrimoniales@riouruguay.com.ar"],
            },
            "PATRIMONIALES FAST TRACK": {
                "Descripción": "Este equipo gestionará siniestros de Riesgos Patrimoniales (Lo que no es fast track). Los ramos que incluye son Hogar y Comercio con sus coberturas de Robo, Daños por agua y Incendio. Bolsa CRM: Siniestros Patrimoniales - Fast Track",
                "Correo": ["siniestrosfasttrack@riouruguay.com.ar"],
            },
            "RIESGOS ESPECIALES FAST TRACK": {
                "Descripción": "Este equipo gestionará siniestros de Riesgos Agrícolas y Caútion. Bolsa CRM: Siniestros Fast Track - Riesgos Especiales",
                "Correo": ["siniestrosfasttrack@riouruguay.com.ar"],
            },
            "PATRIMONIALES VARIAS": {
                "Descripción": "Este equipo gestionará siniestros de Riesgos Patrimoniales (Lo que no es fast track). Los ramos que incluye son Hogar y Comercio con sus coberturas de Robo, Daños por agua y Incendio. Bolsa CRM: Siniestros Patrimoniales - Varias",
                "Correo": ["siniestrospatrimoniales@riouruguay.com.ar"],
            },
            "FASTTRACK VARIAS": {
                "Descripción": "Este equipo gestionará siniestros de cristales, daños electrodomésticos, TV audio y video, Tecnología y Micromovilidad Bolsa CRM: Siniestros Varias • Fast Track",
                "Correo": ["siniestrosvariasexpress@riouruguay.com.ar"],
            },
            "LESIONES - VIDA Y SALUD": {
                "Descripción": "Este equipo gestionará los siniestros de Seguros de Personas ás los que afecten la cobertura de Responsabilidad Civil de cualquier ramo (excepto auto y moto). Los ramos que incluye son: Salud. Vida (Vida Individual. Vida Colectivo y Vida Obligatorio), Sepelio, Accidentes Personales y Responsabilidad Bolsa CRM: Siniestros Varias - Personas",
                "Correo": ["siniestrosdepersonas@riouruguay.com.ar"],
            },
        },
    }

    def call_phone(self, phone_number):
        def handle_click(e):
            # whatsapp://send?phone=214324234
            # self.page.launch_url(f"whatsapp://send?phone={phone_number}")
            self.page.launch_url(f"tel:{phone_number}")

        return handle_click

    def copy_number(self, phone_number):
        def handle_click(e):
            self.page.set_clipboard(phone_number)
            self.page.open(self.snack_bar_phone)

        return handle_click

    def copy_mail(self, mail):
        def handle_click(e):
            self.page.set_clipboard(mail)
            self.page.open(self.snack_bar_mail)

        return handle_click

    def create_phone_list(self):
        sections = []

        for title, contacts_list in self.telefonos_titulos.items():
            contacts = contacts_list[0]

            section = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.PRIMARY,
                        ),
                        ft.Divider(
                            height=1,
                            color=ft.colors.PRIMARY_CONTAINER,
                        ),
                        ft.Column(
                            controls=[
                                ft.ListTile(
                                    title=ft.Text(
                                        name,
                                        color=ft.colors.ON_SURFACE,
                                    ),
                                    subtitle=ft.Container(
                                        content=ft.Text(
                                            number,
                                            color=ft.colors.PRIMARY,
                                        ),
                                        on_click=self.copy_number(number),
                                        tooltip="Click para copiar",
                                    ),
                                    trailing=ft.IconButton(
                                        icon=ft.icons.CALL,
                                        icon_color=ft.colors.SECONDARY,
                                        tooltip="Llamar",
                                        on_click=self.call_phone(number),
                                    ),
                                )
                                for name, number in contacts.items()
                            ],
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.all(10),
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            )
            sections.append(section)

        return sections

    def create_emails_section(self):
        sections = []
        for category, contacts in self.correos_data.items():
            section = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            category,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.PRIMARY,
                        ),
                        ft.Divider(height=1, color=ft.colors.PRIMARY_CONTAINER),
                        *[
                            ft.ListTile(
                                title=ft.Row(
                                    [
                                        ft.Text(name, color=ft.colors.ON_SURFACE),
                                        ft.Container(
                                            content=ft.IconButton(
                                                ft.icons.EMAIL,
                                                on_click=lambda e: self.page.launch_url(
                                                    f"mailto:{info["Correo"][0]}"
                                                ),
                                                padding=0,
                                                width=30,
                                                height=30,
                                                icon_size=20,
                                            ),
                                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                                            border_radius=100,
                                        ),
                                    ],
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                subtitle=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                info["Descripción"],
                                                size=12,
                                                color=ft.colors.ON_SURFACE_VARIANT,
                                            ),
                                            *[
                                                ft.Container(
                                                    content=ft.Text(
                                                        email, color=ft.colors.PRIMARY
                                                    ),
                                                    on_click=self.copy_mail(email),
                                                    tooltip="Click para copiar",
                                                )
                                                for email in info["Correo"]
                                            ],
                                        ]
                                    ),
                                ),
                            )
                            for name, info in contacts.items()
                        ],
                    ],
                    spacing=10,
                ),
                padding=ft.padding.all(10),
                margin=ft.margin.only(bottom=10),
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            )
            sections.append(section)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Directorio de Correos",
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        color=ft.colors.PRIMARY,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(height=2, color=ft.colors.PRIMARY_CONTAINER),
                    ft.Container(
                        content=ft.Column(controls=sections, scroll=ft.ScrollMode.AUTO),
                        expand=True,
                    ),
                ],
                spacing=20,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )

    def create_pages_section(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Sección de Páginas",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.PRIMARY,
                    ),
                    ft.Text(
                        "Contenido próximamente",
                        color=ft.colors.ON_SURFACE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    def __init__(self):
        super().__init__()
        self.tab_alignment = ft.TabAlignment.CENTER
        self.expand = True

        # Crear el SnackBar para las notificaciones
        self.snack_bar_phone = ft.SnackBar(
            content=ft.Text("¡Número copiado al portapapeles!"),
            action="OK",
            action_color=ft.colors.SECONDARY,
        )

        self.snack_bar_mail = ft.SnackBar(
            content=ft.Text("¡Correo copiado al portapapeles!"),
            action="OK",
            action_color=ft.colors.SECONDARY,
        )

        # Crear el contenido de la pestaña de teléfonos
        phone_list = self.create_phone_list()
        phones_content = ft.Container(
            expand=True,
            padding=10,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Directorio Telefónico",
                            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            color=ft.colors.PRIMARY,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(
                            height=2,
                            color=ft.colors.PRIMARY_CONTAINER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=phone_list,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,
                        ),
                        self.snack_bar_phone,  # Agregar el SnackBar al contenido
                    ],
                    spacing=10,
                ),
                # padding=ft.padding.all(5),
                # expand=True,
            ),
        )

        # Configurar las pestañas
        self.tabs = [
            ft.Tab(
                text="Premio",
                icon=ft.icons.ATTACH_MONEY,
                content=CalculadoraPremio()),
            ft.Tab(
                text="Teléfonos",
                icon=ft.icons.PHONE,
                content=phones_content,
            ),
            ft.Tab(
                text="Correos",
                icon=ft.icons.EMAIL,
                content=self.create_emails_section(),
            ),
            ft.Tab(
                text="Páginas",
                icon=ft.icons.WEB,
                content=self.create_pages_section(),
            ),
        ]


def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    page.title = "Utilidades"
    page.theme_mode = ft.ThemeMode.DARK
    page.locale_configuration = ft.LocaleConfiguration(
        [ft.Locale("es", "ES")],
        current_locale=ft.Locale("es", "ES"),
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
    page.window.width, page.window.height = calcular_alto(380)
    page.window.always_on_top = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    tabs = ft.Tabs(
        [
            # ft.Tab(
            #     text="TEST",
            #     content=ft.Container(
            #         expand=True,
            #         content=RusContactos(),
            #     ),
            # ),
            ft.Tab(
                text="RUS",
                content=ft.Container(
                    expand=True,
                    content=RusContactos(),
                ),
            ),
            ft.Tab(
                text="FED",
                content=ft.Container(
                    ft.Tabs(
                        [
                            TabFederacionFranquicias(),
                            
                        ],
                        tab_alignment=ft.TabAlignment.CENTER,
                        expand=True,
                    ),
                    expand=True,
                ),
            ),
            ft.Tab(
                text="GENERAL",
                content=ft.Container(
                    ft.Tabs(
                        [
                            TabGeneralPatentes(),
                            ft.Tab(text="Contador Billetes", content=Billetes()),
                            ft.Tab(text="Server", content=FileUploader()),
                            ft.Tab(text="ChatBot", content=ChatBot(
                                    token="AIzaSyCTpmY_rKZLlWc-AnnyjUqbj5SHrfG3NWo",
                                    bot_name=f"ChatBot",
                                    user_name="Usuario",
                                    json_path=f"chat_history.json",
                                    autofocus=False,
                                    font_family="GasoekOne"
                                )
                            )
                            
                        ],
                        tab_alignment=ft.TabAlignment.CENTER,
                        expand=True,
                    ),
                    expand=True,
                ),
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
                        expand=True,
                    ),
                    expand=True,
                ),
            ),
        ],
        expand=True,
        tab_alignment=ft.TabAlignment.CENTER,
    )
    page.add(ft.SafeArea(expand=True, content=tabs))


ft.app(
    target=main,
    upload_dir="assets/uploads",
    view=ft.AppView.WEB_BROWSER,
    assets_dir="assets",
)
