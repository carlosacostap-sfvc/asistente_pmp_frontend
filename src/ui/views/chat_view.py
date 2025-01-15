import flet as ft
from typing import Callable, List
from src.services.chat_service import chat_service
from src.ui.components import ChatMessage, create_title, create_container

class ChatView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.messages: List[ChatMessage] = []
        self.page = None

    def create_message_container(self, message: ChatMessage) -> ft.Container:
        """Crea un contenedor de mensaje con el nuevo diseño."""
        is_user = message.message_type == "user"
        return ft.Container(
            content=ft.Column([
                # Encabezado del mensaje con nombre y hora
                ft.Row([
                    ft.Icon(
                        ft.icons.PERSON if is_user else ft.icons.SMART_TOY,
                        color=ft.colors.GREY_700,
                        size=16,
                    ),
                    ft.Text(
                        message.user_name,
                        size=12,
                        color=ft.colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Text(
                        message.timestamp,
                        size=10,
                        color=ft.colors.GREY_500,
                    )
                ], spacing=4),
                # Contenido del mensaje
                ft.Container(
                    content=ft.Text(
                        message.text,
                        size=14,
                        color=ft.colors.BLACK if is_user else ft.colors.BLACK,
                        weight=ft.FontWeight.W_400,
                        selectable=True,
                    ),
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=8,
                ),
            ]),
            margin=ft.margin.only(left=0 if is_user else 20, right=20 if is_user else 0),
        )

    def create_chat_header(self) -> ft.Container:
        """Crea el encabezado del chat con el nuevo diseño."""
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.CHAT_OUTLINED, size=24, color=ft.colors.BLUE),
                        margin=ft.margin.only(right=15),
                    ),
                    ft.Column([
                        ft.Text(
                            "Chat con GPT",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            "Resuelve tus dudas sobre gestión de proyectos",
                            size=14,
                            color=ft.colors.GREY_700,
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
        )

    def create_chat_container(self) -> ft.Container:
        """Crea el contenedor principal del chat con el nuevo diseño."""
        self.chat_history = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400,
            auto_scroll=True
        )

        return ft.Container(
            content=self.chat_history,
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
        )

    def create_input_container(self) -> ft.Container:
        """Crea el contenedor de entrada de mensajes con el nuevo diseño."""
        self.new_message = ft.TextField(
            hint_text="Escribe tu mensaje aquí...",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            text_size=14,
            min_lines=1,
            max_lines=5,
            multiline=True,
            expand=True,
            on_submit=self.handle_send_message,
            text_style=ft.TextStyle(
                color=ft.colors.BLACK,
                size=14,
                weight=ft.FontWeight.W_500
            ),
        )

        self.send_button = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            icon_color=ft.colors.BLUE,
            icon_size=24,
            on_click=self.handle_send_message,
        )

        return ft.Container(
            content=ft.Row([
                self.new_message,
                self.send_button,
            ], spacing=10),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
        )

    def add_message(self, text: str, message_type: str):
        """Añade un mensaje al historial del chat."""
        user_name = "Tú" if message_type == "user" else "Asistente"
        message = ChatMessage(user_name=user_name, text=text, message_type=message_type)
        self.messages.append(message)
        self.chat_history.controls.append(self.create_message_container(message))
        self.page.update()

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.bgcolor = ft.colors.GREY_50
        page.padding = 40
        page.scroll = ft.ScrollMode.AUTO

        # Botón de retorno
        return_button = ft.TextButton(
            content=ft.Row([
                ft.Icon(ft.icons.ARROW_BACK, color=ft.colors.BLUE),
                ft.Text("Volver al Inicio", color=ft.colors.BLUE),
            ]),
            on_click=self.handle_return,
        )

        # Contenido principal
        content = ft.Column([
            create_title("Chat Asistente PMP"),
            ft.Text(
                "Consulta tus dudas sobre la preparación del examen PMP",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Contenedores principales
            self.create_chat_header(),
            self.create_chat_container(),
            self.create_input_container(),
            return_button,
        ])

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()

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
            ft.Text("El asistente está escribiendo...", italic=True, size=12)
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
        chat_service.clear_history()
        self.on_return_home(e)