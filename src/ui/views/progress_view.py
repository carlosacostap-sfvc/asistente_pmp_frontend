import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button
from src.services.api_service import api_service

class ProgressView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Obtener el email del usuario actual
        user_email = api_service.current_user.email if api_service.current_user else "Usuario"

        # Crear los elementos de la UI
        content = ft.Column(
            controls=[
                create_title("Mi Progreso"),
                ft.Text(
                    f"Bienvenido a tu progreso, {user_email}",
                    size=16,
                    color=ft.colors.BLUE_GREY_700,
                ),
                create_button(
                    text="Volver al inicio",
                    on_click=self.on_return_home,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Crear el contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()