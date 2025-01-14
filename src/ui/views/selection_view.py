import flet as ft
from src.ui.components import create_title, create_container, create_button

class SelectionView:
    def __init__(
        self,
        on_practice_selected,
        on_chat_selected,
        on_progress_selected,
        on_educational_resources_selected,  # Nuevo callback
        on_logout
    ):
        self.on_practice_selected = on_practice_selected
        self.on_chat_selected = on_chat_selected
        self.on_progress_selected = on_progress_selected
        self.on_educational_resources_selected = on_educational_resources_selected  # Nuevo
        self.on_logout = on_logout
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.title = "Selección de Modo"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.clean()

        # Botones de opción
        chat_button = create_button(
            text="Chat con GPT",
            on_click=self.handle_chat,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        )

        practice_button = create_button(
            text="Práctica PMP",
            on_click=self.handle_practice,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        educational_resources_button = create_button(
            text="Recursos Educativos",
            on_click=self.handle_educational_resources,
            bgcolor=ft.colors.ORANGE,  # Color distintivo
            color=ft.colors.WHITE,
        )

        progress_button = create_button(
            text="Mi Progreso",
            on_click=self.handle_progress,
            bgcolor=ft.colors.PURPLE,
            color=ft.colors.WHITE,
        )

        logout_button = create_button(
            text="Cerrar Sesión",
            on_click=self.handle_logout,
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
        )

        content = ft.Column(
            controls=[
                create_title("¿Qué te gustaría hacer?"),
                ft.Text(
                    "Selecciona una opción para continuar",
                    size=16,
                    color=ft.colors.BLUE_GREY_700,
                ),
                practice_button,
                chat_button,
                progress_button,
                educational_resources_button,  # Nuevo botón
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                logout_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    def handle_chat(self, e):
        self.on_chat_selected(e)

    async def handle_practice(self, e):
        await self.on_practice_selected(e)

    def handle_educational_resources(self, e):
        """Maneja la navegación a la vista de recursos educativos"""
        self.on_educational_resources_selected(e)

    def handle_progress(self, e):
        """Maneja la navegación a la vista de progreso"""
        self.on_progress_selected(e)

    async def handle_logout(self, e):
        await self.on_logout(e)