import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button

class EducationalResourcesView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO

        # Función para crear una tarjeta de recurso con texto en negro
        def create_resource_card(title: str, description: str, icon: str) -> ft.Container:
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(icon, size=24, color=ft.colors.BLUE),
                        ft.Text(
                            title,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK
                        )
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Text(
                        description,
                        size=14,
                        color=ft.colors.BLACK
                    ),
                    ft.TextButton(
                        text="Ver más",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e: self.handle_pmbok_principles(e) if title == "Guía PMBOK 7ma Edición" else None,
                        style=ft.ButtonStyle(
                            color=ft.colors.BLUE
                        )
                    )
                ]),
                padding=20,
                margin=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                border=ft.border.all(1, ft.colors.BLUE_200),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.BLACK12,
                )
            )

        # Guías basadas en PMBOK
        pmbok_guides = ft.Column([
            ft.Text(
                "Guías de Estudio basadas en el PMBOK",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK
            ),
            create_resource_card(
                "Guía PMBOK 7ma Edición",
                "Resumen completo de los 12 principios del Project Management según el PMBOK 7",
                ft.icons.BOOK
            ),
            create_resource_card(
                "Principios de Gestión",
                "Explicación detallada de cada principio con ejemplos prácticos",
                ft.icons.LIGHTBULB
            ),
        ])

        # Guías basadas en Dominios
        domain_guides = ft.Column([
            ft.Text(
                "Guías de Estudio basadas en los Dominios",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK
            ),
            create_resource_card(
                "Personas",
                "Guía completa del dominio de Personas con ejemplos y casos de estudio",
                ft.icons.PEOPLE
            ),
            create_resource_card(
                "Procesos",
                "Guía detallada del dominio de Procesos con ejemplos prácticos",
                ft.icons.ACCOUNT_TREE
            ),
            create_resource_card(
                "Entorno de Negocio",
                "Guía exhaustiva del dominio de Entorno de Negocio con casos reales",
                ft.icons.BUSINESS
            ),
        ])

        # Recursos en Video
        video_resources = ft.Column([
            ft.Text(
                "Recursos en Video",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK
            ),
            create_resource_card(
                "Video Tutoriales",
                "Explicaciones paso a paso de conceptos clave del PMP",
                ft.icons.PLAY_CIRCLE
            ),
            create_resource_card(
                "Webinars Grabados",
                "Sesiones con expertos PMP sobre temas específicos",
                ft.icons.VIDEO_LIBRARY
            ),
        ])

        # Botón de retorno
        return_button = create_button(
            text="Volver al inicio",
            on_click=self.on_return_home,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        # Contenido principal
        content = ft.Column(
            controls=[
                create_title("Recursos Educativos"),
                ft.Text(
                    "Explora nuestra colección de recursos para prepararte para el examen PMP",
                    size=16,
                    color=ft.colors.BLACK,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                pmbok_guides,
                ft.Divider(),
                domain_guides,
                ft.Divider(),
                video_resources,
                return_button,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    def handle_resource_click(self, resource_title: str):
        """Maneja el click en un recurso específico"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Próximamente: {resource_title}"),
                action="OK"
            )
        )

    def handle_pmbok_principles(self, e):
        """Maneja la navegación a la vista de principios del PMBOK"""
        from src.ui.views.pmbok_principles_view import PMBOKPrinciplesView
        principles_view = PMBOKPrinciplesView(
            on_return_to_resources=lambda e: self.build(self.page)
        )
        principles_view.build(self.page)