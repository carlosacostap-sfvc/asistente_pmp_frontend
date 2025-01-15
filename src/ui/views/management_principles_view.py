# src/ui/views/management_principles_view.py
import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button
from src.data.principles_data import PRINCIPLES_DATA


class ManagementPrinciplesView:
    def __init__(self, on_return_to_resources: Callable):
        self.on_return_to_resources = on_return_to_resources
        self.page = None

    def create_principle_card(self, principle: dict) -> ft.Container:
        """Crea una tarjeta para mostrar un principio."""
        return ft.Container(
            content=ft.Column([
                # Encabezado con número y título
                ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(
                            str(principle["number"]),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE
                        ),
                        bgcolor=ft.colors.BLUE,
                        radius=15,
                    ),
                    ft.Text(
                        principle["title"],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                    )
                ], alignment=ft.MainAxisAlignment.START, spacing=10),

                # Descripción
                ft.Text(
                    principle["description"],
                    size=14,
                    color=ft.colors.BLACK,
                ),

                # Botón ver detalles
                ft.TextButton(
                    text="Ver detalles",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_principle_detail(principle),
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE
                    )
                )
            ]),
            padding=20,
            margin=ft.margin.only(bottom=10),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLUE_200),
            ink=True,
        )

    def show_principle_detail(self, principle: dict):
        """Muestra el detalle de un principio específico."""
        self.page.clean()

        content = ft.Column([
            # Encabezado
            ft.Row([
                ft.CircleAvatar(
                    content=ft.Text(
                        str(principle["number"]),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    ),
                    bgcolor=ft.colors.BLUE,
                    radius=25,
                ),
                ft.Text(
                    principle["title"],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=20),

            ft.Divider(),

            # Descripción
            ft.Container(
                content=ft.Column([
                    ft.Text("Descripción",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK),
                    ft.Text(principle["description"],
                            size=16,
                            color=ft.colors.BLACK)
                ]),
                padding=20,
                bgcolor=ft.colors.BLUE_50,
                border_radius=10,
            ),

            # Ejemplos
            ft.Container(
                content=ft.Column([
                    ft.Text("Ejemplos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK),
                    *[
                        ft.Row([
                            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE,
                                    color=ft.colors.GREEN),
                            ft.Text(example, size=16, color=ft.colors.BLACK)
                        ])
                        for example in principle["examples"]
                    ]
                ]),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                border=ft.border.all(1, ft.colors.BLUE_200),
            ),

            # Puntos clave
            ft.Container(
                content=ft.Column([
                    ft.Text("Puntos Clave",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK),
                    *[
                        ft.Row([
                            ft.Icon(ft.icons.STAR_OUTLINE,
                                    color=ft.colors.ORANGE),
                            ft.Text(point, size=16, color=ft.colors.BLACK)
                        ])
                        for point in principle["key_points"]
                    ]
                ]),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                border=ft.border.all(1, ft.colors.BLUE_200),
            ),

            # Botón de retorno
            create_button(
                text="Volver a la lista de principios",
                on_click=lambda e: self.build(self.page),
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
        ], scroll=ft.ScrollMode.AUTO, spacing=20)

        container = create_container(content)
        self.page.add(container)
        self.page.update()

    def build(self, page: ft.Page):
        """Construye la vista principal de principios."""
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO

        content = ft.Column([
            create_title("Principios de Gestión de Proyectos"),
            ft.Text(
                "Estos principios fundamentales guían la gestión efectiva de proyectos según el PMBOK 7.",
                size=16,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_500
            ),
            ft.Column([
                self.create_principle_card(principle)
                for principle in PRINCIPLES_DATA
            ], spacing=10),
            create_button(
                text="Volver a Recursos",
                on_click=self.on_return_to_resources,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            )
        ], spacing=20)

        container = create_container(content)
        page.add(container)
        page.update()