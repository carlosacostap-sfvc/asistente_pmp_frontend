import flet as ft
from typing import Callable
from src.services.chat_service import chat_service
from src.ui.components import ChatMessage, create_message_container, create_button


class PrincipleChatView:
    def __init__(self, principle_number: int, title: str, description: str, on_return_to_principles: Callable):
        self.principle_number = principle_number
        self.title = title
        self.description = description
        self.on_return_to_principles = on_return_to_principles
        self.messages = []
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.padding = 20
        page.spacing = 20
        page.window_width = 800
        page.window_min_width = 600

        # Historial de chat
        self.chat_history = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        # Campo de mensaje
        self.new_message = ft.TextField(
            hint_text="Escribe tu pregunta sobre este principio...",
            border_color=ft.colors.BLUE,
            expand=True,
            min_lines=1,
            max_lines=5,
            multiline=True,
            on_submit=self.handle_send_message,
            text_style=ft.TextStyle(size=14),
        )

        # Botones
        self.send_button = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_send_message
        )

        self.return_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_return
        )

        # Contenedor principal
        main_container = ft.Container(
            expand=True,
            content=ft.Column([
                # Barra superior
                ft.Row([
                    self.return_button,
                    ft.Text(
                        f"Chat sobre Principio {self.principle_number}",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                ], alignment=ft.MainAxisAlignment.START),

                # Área de chat
                ft.Container(
                    content=self.chat_history,
                    border=ft.border.all(1, ft.colors.BLUE_GREY_400),
                    border_radius=10,
                    padding=20,
                    expand=True,
                    width=float("inf"),
                ),

                # Área de entrada
                ft.Container(
                    content=ft.Row([
                        self.new_message,
                        self.send_button
                    ], spacing=10),
                    width=float("inf")
                )
            ], expand=True, spacing=20)
        )

        page.add(main_container)

        # Enviar mensaje de bienvenida
        self.page.loop.create_task(self.send_welcome_message())
        page.update()

    async def send_welcome_message(self):
        welcome_message = (
            f"👋 ¡Bienvenido al chat sobre el Principio {self.principle_number}!\n\n"
            f"**{self.title}**\n\n"
            f"{self.description}\n\n"
            "Estoy aquí para ayudarte a comprender mejor este principio. "
            "Puedes hacerme preguntas específicas sobre su aplicación, ejemplos "
            "prácticos o cualquier duda que tengas sobre este tema."
        )

        self.add_message(welcome_message, "bot")

    def add_message(self, text: str, message_type: str):
        """Añade un mensaje al historial del chat."""
        user_name = "Tú" if message_type == "user" else "Asistente"
        message = ChatMessage(user_name=user_name, text=text, message_type=message_type)
        self.messages.append(message)
        self.chat_history.controls.append(create_message_container(message))
        self.page.update()

    async def handle_send_message(self, e):
        """Maneja el envío de mensajes."""
        if not self.new_message.value:
            return

        user_text = self.new_message.value
        self.new_message.value = ""
        self.page.update()

        # Mostrar el mensaje del usuario
        self.add_message(user_text, "user")

        # Mostrar indicador de escritura
        typing_indicator = ft.Row([
            ft.ProgressRing(width=16, height=16),
            ft.Text("Escribiendo...", italic=True, size=12)
        ], spacing=10)
        self.chat_history.controls.append(typing_indicator)
        self.page.update()

        try:
            # Crear el contexto para el principio específico
            context = (
                f"Estamos discutiendo específicamente sobre el Principio {self.principle_number} "
                f"del PMBOK 7: {self.title}. {self.description} "
                "Por favor, mantén las respuestas enfocadas en este principio y sus aplicaciones."
            )

            # Enviar mensaje con el contexto
            response = await chat_service.send_message(
                f"Contexto: {context}\n\nPregunta del usuario: {user_text}"
            )

            if response.startswith("Error: Sesión expirada"):
                self.on_return_to_principles(e)
                return

            # Mostrar la respuesta
            self.add_message(response, "bot")

        finally:
            # Remover indicador de escritura
            if typing_indicator in self.chat_history.controls:
                self.chat_history.controls.remove(typing_indicator)
            self.page.update()

    def handle_return(self, e):
        """Maneja el regreso a la vista de principios."""
        self.on_return_to_principles(e)