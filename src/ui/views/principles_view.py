import flet as ft
from typing import Callable, Optional
from src.ui.components import create_title, create_container

class PrinciplesView:
    def __init__(
        self,
        on_return_home: Callable,
        on_principle_detail: Optional[Callable] = None
    ):
        self.on_return_home = on_return_home
        self.on_principle_detail = on_principle_detail
        self.page = None
        self.principles = [
            {
                "number": 1,
                "title": "Ser un administrador diligente",
                "description": "Demuestra comportamiento ético y responsable",
                "icon": ft.icons.ADMIN_PANEL_SETTINGS,
                "has_detail": True
            },
            {
                "number": 2,
                "title": "Crear un ambiente colaborativo",
                "description": "Fomenta el trabajo en equipo efectivo",
                "icon": ft.icons.GROUP_WORK,
                "has_detail": True
            },
            {
                "number": 3,
                "title": "Involucrar a los interesados",
                "description": "Gestiona expectativas y comunicación",
                "icon": ft.icons.PEOPLE_OUTLINE,
                "has_detail": False
            },
            {
                "number": 4,
                "title": "Enfocarse en el valor",
                "description": "Prioriza la entrega de beneficios",
                "icon": ft.icons.TRENDING_UP,
                "has_detail": False
            },
            {
                "number": 5,
                "title": "Reconocer interacciones del sistema",
                "description": "Gestiona dependencias e impactos",
                "icon": ft.icons.HUB,
                "has_detail": False
            },
            {
                "number": 6,
                "title": "Demostrar liderazgo",
                "description": "Guía y motiva al equipo",
                "icon": ft.icons.EMOJI_EVENTS,
                "has_detail": False
            },
            {
                "number": 7,
                "title": "Adaptar según el contexto",
                "description": "Ajusta el enfoque según necesidades",
                "icon": ft.icons.TUNE,
                "has_detail": False
            },
            {
                "number": 8,
                "title": "Incorporar la calidad",
                "description": "Asegura estándares en entregables",
                "icon": ft.icons.VERIFIED,
                "has_detail": False
            },
            {
                "number": 9,
                "title": "Navegar en la complejidad",
                "description": "Gestiona situaciones complejas",
                "icon": ft.icons.ACCOUNT_TREE,
                "has_detail": False
            },
            {
                "number": 10,
                "title": "Optimizar respuestas a riesgos",
                "description": "Gestiona amenazas y oportunidades",
                "icon": ft.icons.SECURITY,
                "has_detail": False
            },
            {
                "number": 11,
                "title": "Adoptar adaptabilidad",
                "description": "Mantiene flexibilidad ante cambios",
                "icon": ft.icons.AUTO_MODE,
                "has_detail": False
            },
            {
                "number": 12,
                "title": "Permitir el cambio",
                "description": "Facilita la transición efectiva",
                "icon": ft.icons.CHANGE_CIRCLE,
                "has_detail": False
            }
        ]

    def create_principle_card(self, principle: dict) -> ft.Container:
        """Crea una tarjeta para un principio con el estilo de la aplicación."""
        content = ft.Row([
            # Contenido principal
            ft.Row([
                # Ícono y número
                ft.Container(
                    content=ft.Stack([
                        ft.Icon(
                            principle["icon"],
                            size=24,
                            color=ft.colors.BLUE
                        ),
                        ft.Container(
                            content=ft.Text(
                                str(principle["number"]),
                                size=12,
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            bgcolor=ft.colors.BLUE,
                            border_radius=8,
                            padding=5,
                            margin=ft.margin.only(left=20, top=20),
                        )
                    ]),
                    width=48,
                    height=48,
                ),
                # Textos
                ft.Column([
                    ft.Text(
                        principle["title"],
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        principle["description"],
                        size=14,
                        color=ft.colors.GREY_700,
                    ),
                ],
                spacing=5,
                expand=True,
                ),
            ], expand=True),
            # Flecha derecha (solo si tiene vista detallada)
            ft.Icon(
                ft.icons.ARROW_FORWARD_IOS,
                size=20,
                color=ft.colors.GREY_400,
            ) if principle.get("has_detail") else ft.Container(),
        ])

        container = ft.Container(
            content=content,
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            ink=True if principle.get("has_detail") else False,
            on_click=lambda e, p=principle: self.handle_principle_click(e, p) if p.get("has_detail") else None,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

        # Si el principio no tiene detalle, agregar un mensaje de "próximamente"
        if not principle.get("has_detail"):
            container = ft.Container(
                content=ft.Stack([
                    container,
                    ft.Container(
                        content=ft.Text(
                            "Próximamente",
                            size=12,
                            color=ft.colors.WHITE,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=ft.colors.GREY_700,
                        border_radius=5,
                        padding=ft.padding.all(5),
                        alignment=ft.alignment.center,
                    ),
                ]),
            )

        return container

    def handle_principle_click(self, e, principle: dict):
        """Maneja el clic en un principio."""
        if principle.get("has_detail") and self.on_principle_detail:
            self.on_principle_detail(e, principle["number"])

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.bgcolor = ft.colors.GREY_50

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("Los 12 Principios del PMBOK 7"),
            ft.Text(
                "Fundamentos esenciales para la gestión efectiva de proyectos",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Lista de principios
            ft.Column([
                self.create_principle_card(principle)
                for principle in self.principles
            ], spacing=10),

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

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()