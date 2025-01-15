import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container

class PrinciplesView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.page = None
        self.principles = [
            {
                "number": 1,
                "title": "Ser un administrador diligente",
                "description": "Demuestra comportamiento ético y responsable",
                "icon": ft.icons.ADMIN_PANEL_SETTINGS
            },
            {
                "number": 2,
                "title": "Crear un ambiente colaborativo",
                "description": "Fomenta el trabajo en equipo efectivo",
                "icon": ft.icons.GROUP_WORK
            },
            {
                "number": 3,
                "title": "Involucrar a los interesados",
                "description": "Gestiona expectativas y comunicación",
                "icon": ft.icons.PEOPLE_OUTLINE
            },
            {
                "number": 4,
                "title": "Enfocarse en el valor",
                "description": "Prioriza la entrega de beneficios",
                "icon": ft.icons.TRENDING_UP
            },
            {
                "number": 5,
                "title": "Reconocer interacciones del sistema",
                "description": "Gestiona dependencias e impactos",
                "icon": ft.icons.HUB
            },
            {
                "number": 6,
                "title": "Demostrar liderazgo",
                "description": "Guía y motiva al equipo",
                "icon": ft.icons.EMOJI_EVENTS
            },
            {
                "number": 7,
                "title": "Adaptar según el contexto",
                "description": "Ajusta el enfoque según necesidades",
                "icon": ft.icons.TUNE
            },
            {
                "number": 8,
                "title": "Incorporar la calidad",
                "description": "Asegura estándares en entregables",
                "icon": ft.icons.VERIFIED
            },
            {
                "number": 9,
                "title": "Navegar en la complejidad",
                "description": "Gestiona situaciones complejas",
                "icon": ft.icons.ACCOUNT_TREE
            },
            {
                "number": 10,
                "title": "Optimizar respuestas a riesgos",
                "description": "Gestiona amenazas y oportunidades",
                "icon": ft.icons.SECURITY
            },
            {
                "number": 11,
                "title": "Adoptar adaptabilidad",
                "description": "Mantiene flexibilidad ante cambios",
                "icon": ft.icons.AUTO_MODE
            },
            {
                "number": 12,
                "title": "Permitir el cambio",
                "description": "Facilita la transición efectiva",
                "icon": ft.icons.CHANGE_CIRCLE
            }
        ]

    def create_principle_card(self, principle: dict) -> ft.Container:
        """Crea una tarjeta para un principio con el estilo de la aplicación."""
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(
                            principle["icon"],
                            size=24,
                            color=ft.colors.BLUE
                        ),
                        margin=ft.margin.only(right=15),
                    ),
                    ft.Column([
                        ft.Text(
                            f"{principle['number']}. {principle['title']}",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            principle["description"],
                            size=14,
                            color=ft.colors.GREY_700,
                            width=400,
                        ),
                    ],
                    spacing=5,
                    ),
                ], expand=True),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.bgcolor = ft.colors.GREY_50

        content = ft.Column([
            create_title("Los 12 Principios de la Gestión de Proyectos"),
            ft.Text(
                "Fundamentos del PMBOK 7ma Edición",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Lista de principios
            *[self.create_principle_card(principle) for principle in self.principles],

            # Botón de retorno
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=ft.colors.BLUE,
                        on_click=self.on_return_home,
                    ),
                    ft.Text(
                        "Volver al Inicio",
                        color=ft.colors.BLUE,
                        weight=ft.FontWeight.W_500,
                        size=16,
                    ),
                ]),
                on_click=self.on_return_home,
                ink=True,
            ),
        ])

        container = create_container(content)
        page.add(container)
        page.update()