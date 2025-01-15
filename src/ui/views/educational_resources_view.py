import flet as ft
from typing import Callable, Optional
from src.ui.components import create_title, create_container, create_button

class EducationalResourcesView:
    def __init__(self, on_return_home: Callable, on_principles_selected: Optional[Callable] = None):
        self.on_return_home = on_return_home
        self.on_principles_selected = on_principles_selected
        self.page = None

    def create_resource_card(self, icon: str, title: str, description: str, on_click=None) -> ft.Container:
        """Crea una tarjeta de recurso con el nuevo diseño."""
        return ft.Container(
            content=ft.Row([
                # Contenido principal
                ft.Row([
                    # Ícono
                    ft.Container(
                        content=ft.Icon(icon, size=24, color=ft.colors.BLUE),
                        margin=ft.margin.only(right=15),
                    ),
                    # Textos
                    ft.Column([
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            description,
                            size=14,
                            color=ft.colors.GREY_700,
                            width=400,
                        ),
                    ],
                    spacing=5,
                    ),
                ], expand=True),
                # Flecha derecha
                ft.Icon(
                    ft.icons.ARROW_FORWARD_IOS,
                    size=20,
                    color=ft.colors.GREY_400,
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            ink=True,
            on_click=on_click,
        )

    def create_section_title(self, text: str) -> ft.Text:
        """Crea un título de sección."""
        return ft.Text(
            text,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK,
        )

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("Recursos Educativos"),
            ft.Text(
                "Explora nuestra colección de recursos para prepararte para el examen PMP",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección PMBOK 7ma Edición
            self.create_section_title("Guía de Estudio basada en el PMBOK 7ma Edición"),
            self.create_resource_card(
                ft.icons.RULE_FOLDER,
                "Los 12 Principios de la Gestión de Proyectos",
                "Principios fundamentales que representan la filosofía del PMBOK 7",
                on_click=lambda e: self.on_principles_selected(e) if hasattr(self, 'on_principles_selected') else None
            ),
            self.create_resource_card(
                ft.icons.DASHBOARD_OUTLINED,
                "Los 8 Dominios de Desempeño",
                "Grupos interrelacionados de actividades que influyen en la entrega efectiva de resultados"
            ),
            self.create_resource_card(
                ft.icons.SETTINGS_OUTLINED,
                "Tailoring (Adaptación)",
                "Adaptación de métodos y enfoques según el contexto del proyecto y la organización"
            ),
            self.create_resource_card(
                ft.icons.ARCHITECTURE_OUTLINED,
                "Modelos, Métodos y Artefactos",
                "Para abordar necesidades específicas"
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección Dominios de Evaluación
            self.create_section_title("Guía de Estudio basada en los Dominios de Evaluación en el Examen PMP"),
            self.create_resource_card(
                ft.icons.PEOPLE_OUTLINE,
                "Personas",
                "Gestión de equipos y liderazgo"
            ),
            self.create_resource_card(
                ft.icons.ACCOUNT_TREE_OUTLINED,
                "Procesos",
                "Metodologías y enfoques de gestión"
            ),
            self.create_resource_card(
                ft.icons.BUSINESS_OUTLINED,
                "Entorno de Negocio",
                "Contexto organizacional y entrega de valor"
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección Recursos Complementarios
            self.create_section_title("Recursos Complementarios"),
            ft.Text(
                "Material adicional para tu preparación",
                size=14,
                color=ft.colors.GREY_700,
            ),
            self.create_resource_card(
                ft.icons.PLAY_CIRCLE_OUTLINE_OUTLINED,
                "Video Tutoriales",
                "Explicaciones paso a paso de conceptos clave"
            ),
            self.create_resource_card(
                ft.icons.VIDEO_LIBRARY_OUTLINED,
                "Webinars Grabados",
                "Sesiones con expertos PMP"
            ),

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
        ], spacing=10)

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()

    def handle_resource_click(self, title: str):
        """Maneja el click en un recurso específico."""
        # Mostrar mensaje "Próximamente" para todas las secciones
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Próximamente: {title}"))
        )