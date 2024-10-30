import time

import flet as ft

from components.functions import *
from components.widgets import *


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
                text="GENERAL",
                content=ft.Container(
                    ft.Tabs(
                        [
                            TabGeneralPatentes(),
                            TabFederacionFranquicias(),
                            ft.Tab(text="Contador Billetes", content=Billetes()),
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
