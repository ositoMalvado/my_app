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
        self.files_column = ft.Column(expand=True, scroll="auto")
        
        self.fp = ft.FilePicker(
            on_result=self.handle_file_picked
        )

        # self.upload_button = ft.ElevatedButton("Subir", on_click=self.handle_upload, visible=False)
        
        # Server controls con IP local
        # self.server_status = ft.Text("Apagado", color="red")
        # self.ip_text = ft.Text(f"IP: {self.local_ip}", visible=False)
        self.server_button = ft.ElevatedButton(
            "Encender",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.toggle_server,
            bgcolor=ft.colors.GREEN
        )
        
        self.server_url = ft.TextButton(
            f"http://{self.local_ip}:{self.server_port}",
            icon=ft.icons.OPEN_IN_BROWSER,
            on_click=lambda _: webbrowser.open(f"http://{self.local_ip}:{self.server_port}"),
            visible=False
        )
        
        self.padding=20
        self.margin=10
        self.border_radius=10
        self.border=ft.border.all(1, ft.colors.WHITE24)
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.expand = True

        self.content = ft.Column(
            [
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Archivos",
                            icon=ft.icons.UPLOAD_FILE,
                            expand=True,
                            on_click=lambda _: self.fp.pick_files(
                                allow_multiple=True,
                                allowed_extensions=["jpg", "png", "jpeg", "pdf", "mp4", "mp3", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "bat", "sh", "py", "c", "cpp", "java", "css", "js", "html", "php", "rb", "go", "js", "py", "cs", "json", "xml", "svg", "psd", "ai", "eps", "indd", "ps", "pdf"],
                            ),
                        ),
                        ft.ElevatedButton(
                            "Fotos",
                            icon=ft.icons.ADD_A_PHOTO,
                            expand=True,
                            on_click=lambda _: self.fp.pick_files(
                                allow_multiple=True,
                                # allowed_extensions = [
                                #     "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "svg", "webp",
                                #     "heic", "heif", "apng", "ico", "jfif", "pjpeg", "pjp", "avif", "raw", 
                                #     "cr2", "crw", "nef", "orf", "rw2", "sr2", "arw", "dng", "pef", "raf",
                                #     "eps", "ai", "psd", "indd", "xd", "sketch"
                                # ],
                                file_type=ft.FilePickerFileType.IMAGE
                            ),
                        ),
                    ]
                ),
                self.server_button,
                # ft.Row(
                #     [
                #         self.server_status,
                #         self.ip_text,
                #     ],
                #     alignment=ft.MainAxisAlignment.START
                # ),
                self.server_url,
                # self.upload_button,
                self.files_column
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return
        
        # first of all we remove evry file from assets/uploads
        for f in os.listdir(upload_dir):
            os.remove(os.path.join(upload_dir, f))
        
        
        # self.upload_button.visible = True
        # self.upload_button.update()
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
        self.handle_upload(e)

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
        
        # self.server_status.value = f"Server: Running on port {self.server_port}"
        # self.server_status.color = "green"
        self.server_button.text = "Detener Server"
        self.server_button.icon = ft.icons.STOP
        self.server_button.bgcolor = ft.colors.RED
        self.server_url.visible = True
        # self.ip_text.visible = True
        self.update()

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_server_running = False
            
            # self.server_status.value = "Apagado"
            # self.server_status.color = "red"
            self.server_button.text = "Encender"
            self.server_button.icon = ft.icons.PLAY_ARROW
            self.server_button.bgcolor = ft.colors.GREEN
            self.server_url.visible = False
            # self.ip_text.visible = False
            
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
