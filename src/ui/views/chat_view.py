import flet as ft
from typing import Callable, List
from src.services.chat_service import chat_service
from src.ui.components import ChatMessage, create_message_container

class ChatView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.messages: List[ChatMessage] = []
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.padding = 20
        page.spacing = 20
        page.window_width = 800  # Establecer un ancho mínimo
        page.window_min_width = 600  # Establecer un ancho mínimo

        # Historial de chat
        self.chat_history = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        # Campo de nuevo mensaje
        self.new_message = ft.TextField(
            hint_text="Escribe tu mensaje aquí...",
            border_color=ft.colors.BLUE,
            expand=True,
            min_lines=1,
            max_lines=5,
            multiline=True,
            on_submit=self.handle_send_message,
            text_style=ft.TextStyle(size=14),
        )

        # Botón de enviar
        self.send_button = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_send_message
        )

        # Botón de regresar
        self.return_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_return
        )

        # Contenedor principal que ocupa todo el ancho disponible
        main_container = ft.Container(
            expand=True,
            content=ft.Column([
                # Barra superior
                ft.Row([
                    self.return_button,
                    ft.Text("Chat con GPT", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START),

                # Área de chat (con altura expandible)
                ft.Container(
                    content=self.chat_history,
                    border=ft.border.all(1, ft.colors.BLUE_GREY_400),
                    border_radius=10,
                    padding=20,
                    expand=True,
                    width=float("inf"),  # Usar todo el ancho disponible
                ),

                # Área de entrada (con ancho completo)
                ft.Container(
                    content=ft.Row([
                        self.new_message,
                        self.send_button
                    ], spacing=10),
                    width=float("inf")  # Usar todo el ancho disponible
                )
            ], expand=True, spacing=20)
        )

        page.add(main_container)
        page.update()

    def add_message(self, text: str, message_type: str):
        """Añade un mensaje al historial del chat."""
        user_name = "Tú" if message_type == "user" else "GPT"
        message = ChatMessage(user_name=user_name, text=text, message_type=message_type)
        self.messages.append(message)
        self.chat_history.controls.append(create_message_container(message))
        self.page.update()

    async def handle_send_message(self, e):
        """Maneja el envío de mensajes."""
        if not self.new_message.value:
            return

        # Guardar y limpiar el mensaje del usuario
        user_text = self.new_message.value
        self.new_message.value = ""
        self.page.update()

        # Mostrar el mensaje del usuario
        self.add_message(user_text, "user")

        # Mostrar indicador de escritura
        typing_indicator = ft.Row([
            ft.ProgressRing(width=16, height=16),
            ft.Text("GPT está escribiendo...", italic=True, size=12)
        ], spacing=10)
        self.chat_history.controls.append(typing_indicator)
        self.page.update()

        try:
            # Enviar mensaje y obtener respuesta
            response = await chat_service.send_message(user_text)

            if response.startswith("Error: Sesión expirada"):
                self.on_return_home(e)
                return

            # Mostrar la respuesta
            self.add_message(response, "bot")

        finally:
            # Remover indicador de escritura
            if typing_indicator in self.chat_history.controls:
                self.chat_history.controls.remove(typing_indicator)
            self.page.update()

    def handle_return(self, e):
        """Maneja el regreso a la vista principal."""
        self.on_return_home(e)