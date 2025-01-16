import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button

class PrincipleDetailView2:
    def __init__(self, on_return_to_principles: Callable):
        self.on_return_to_principles = on_return_to_principles
        self.page = None
        self.chat_input = ft.Ref[ft.TextField]()

        # Crear una Column para los mensajes que podamos referenciar
        self.messages_column = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=300,
            auto_scroll=True
        )

        # El contenedor ahora contiene la column
        self.chat_messages_container = ft.Container(
            content=self.messages_column,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            padding=10,
            expand=True
        )

    def create_concept_card(self, title: str, description: str) -> ft.Container:
        """Crea una tarjeta para mostrar un concepto clave."""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    description,
                    size=14,
                    color=ft.colors.BLACK,
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
        )

    def create_keyword_chip(self, text: str) -> ft.Container:
        """Crea un chip para palabras clave."""
        return ft.Container(
            content=ft.Text(
                text,
                size=14,
                color=ft.colors.BLUE_900,
            ),
            padding=ft.padding.all(8),
            border_radius=15,
            bgcolor=ft.colors.BLUE_50,
        )

    def create_practice_question(self) -> ft.Container:
        """Crea la sección de pregunta de práctica."""
        options = [
            "Asignar tareas individualmente a cada miembro del equipo",
            "Fomentar la comunicación abierta y el intercambio de ideas",
            "Establecer reglas estrictas de trabajo",
            "Mantener toda la comunicación por escrito"
        ]

        radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(
                    value=str(i),
                    label=f"{chr(65 + i)}) {opt}",
                    label_style=ft.TextStyle(
                        color=ft.colors.BLACK,
                        size=14,
                    ),
                ) for i, opt in enumerate(options)
            ]),
            on_change=self.handle_option_selected
        )

        explain_button = create_button(
            text="Ver Explicación",
            on_click=self.handle_show_explanation,
            width=150
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Como líder de proyecto, ¿cuál es la mejor manera de crear un ambiente colaborativo en tu equipo?",
                    size=14,
                    color=ft.colors.BLACK,
                ),
                radio_group,
                explain_button,
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
        )

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.bgcolor = ft.colors.GREY_50

        # Botón de retorno
        return_button = ft.TextButton(
            content=ft.Row([
                ft.Icon(ft.icons.ARROW_BACK, color=ft.colors.BLUE),
                ft.Text("Volver a Principios", color=ft.colors.BLUE),
            ]),
            on_click=self.on_return_to_principles,
        )

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("Principio 2: Crear un ambiente colaborativo"),
            ft.Text(
                "Fomenta el trabajo en equipo efectivo y la creación conjunta de valor",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Conceptos Clave
            ft.Text(
                "Conceptos Clave",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK,
            ),
            ft.Row([
                self.create_concept_card(
                    "Liderazgo Participativo",
                    "Promueve la participación activa y el empoderamiento del equipo en la toma de decisiones."
                ),
                self.create_concept_card(
                    "Comunicación Efectiva",
                    "Establece canales claros y mantiene un diálogo abierto entre todos los miembros del equipo."
                ),
            ], wrap=True),
            self.create_concept_card(
                "Cultura de Equipo",
                "Construye un ambiente de confianza, respeto y apoyo mutuo que fomenta la innovación."
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Palabras Clave
            ft.Text(
                "Palabras Clave para el Examen",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK,
            ),
            ft.Row(
                controls=[
                    self.create_keyword_chip(word) for word in [
                        "Colaboración",
                        "Trabajo en equipo",
                        "Comunicación",
                        "Empoderamiento",
                        "Confianza",
                        "Sinergia",
                        "Participación"
                    ]
                ],
                wrap=True,
                spacing=10,
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Tips para el Examen
            ft.Text(
                "Tips para el Examen",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "• Prioriza respuestas que fomenten la colaboración sobre el trabajo individual.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• La comunicación abierta y transparente es clave en un ambiente colaborativo.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• El líder debe actuar como facilitador más que como controlador.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• La diversidad de opiniones y perspectivas enriquece la toma de decisiones.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                ]),
                padding=20,
                bgcolor=ft.colors.ORANGE_50,
                border_radius=8,
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Pregunta de Práctica
            ft.Text(
                "Pregunta de Práctica",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK,
            ),
            self.create_practice_question(),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Chat de Asistencia
            ft.Text(
                "Chat de Asistencia",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLACK,
            ),
            self.create_chat_section(),

            # Botón de retorno
            return_button,
        ])

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()

    def handle_option_selected(self, e):
        """Maneja la selección de una opción en la pregunta de práctica."""
        self.selected_option = e.data
        self.page.update()

    def handle_show_explanation(self, e):
        """Muestra la explicación de la respuesta correcta."""
        if not hasattr(self.page, 'explanation_dialog'):
            self.page.explanation_dialog = ft.AlertDialog(
                title=ft.Text("Explicación de la Respuesta"),
                content=ft.Text(
                    "La respuesta correcta es B) Fomentar la comunicación abierta y el intercambio de ideas.\n\n"
                    "Un ambiente colaborativo se construye sobre la base de una comunicación abierta y el libre "
                    "intercambio de ideas. Asignar tareas individualmente puede limitar la colaboración, las reglas "
                    "estrictas pueden inhibir la creatividad, y mantener toda la comunicación por escrito puede "
                    "hacer el proceso muy formal y menos dinámico."
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog()),
                ],
            )
        self.page.dialog = self.page.explanation_dialog
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Cierra el diálogo de explicación."""
        self.page.dialog.open = False
        self.page.update()

    def create_chat_section(self) -> ft.Container:
        """Crea la sección de chat de asistencia."""
        chat_input_container = ft.Container(
            content=ft.Row([
                ft.TextField(
                    ref=self.chat_input,
                    hint_text="Escribe tu pregunta aquí...",
                    border_radius=8,
                    min_lines=1,
                    max_lines=3,
                    filled=True,
                    expand=True,
                    text_style=ft.TextStyle(
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    hint_style=ft.TextStyle(
                        size=14,
                        color=ft.colors.GREY_600,
                    ),
                    border_color=ft.colors.BLUE_400,
                    focused_border_color=ft.colors.BLUE,
                    focused_bgcolor=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY_50,
                ),
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    icon_color=ft.colors.BLUE,
                    icon_size=24,
                    on_click=self.handle_send_message,
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.BLUE_50,
                        shape=ft.CircleBorder(),
                    ),
                ),
            ], spacing=10),
            padding=ft.padding.only(top=10, bottom=10),
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_200),
            border_radius=8,
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Consulta tus dudas sobre el Principio 2: Crear un ambiente colaborativo",
                    size=14,
                    color=ft.colors.GREY_700,
                ),
                self.chat_messages_container,
                chat_input_container,
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
        )

    async def handle_send_message(self, e):
        """Maneja el envío de mensajes en el chat."""
        if not self.chat_input.current.value:
            return

        message = self.chat_input.current.value
        self.chat_input.current.value = ""
        self.page.update()

        # Mostrar mensaje del usuario
        self.add_chat_message(message, is_user=True)

        # Mostrar indicador de escritura
        typing_indicator = self.create_typing_indicator()
        self.messages_column.controls.append(typing_indicator)
        self.page.update()

        try:
            # Preparar el prompt con contexto del principio
            context_prompt = """
            Estás ayudando con dudas sobre el Principio 2 del PMBOK 7: Crear un ambiente colaborativo.
            Este principio trata sobre el fomento del trabajo en equipo efectivo y la creación conjunta de valor.
            Conceptos clave incluyen: liderazgo participativo, comunicación efectiva y cultura de equipo.
            La consulta del usuario debe ser respondida en este contexto.
            """

            from src.services.chat_service import chat_service
            response = await chat_service.send_message(
                f"{context_prompt}\n\nPregunta del usuario: {message}"
            )

            # Remover indicador de escritura
            if typing_indicator in self.messages_column.controls:
                self.messages_column.controls.remove(typing_indicator)

            # Mostrar respuesta
            if response.startswith("Error"):
                self.add_chat_message(
                    "Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.",
                    is_user=False
                )
            else:
                self.add_chat_message(response, is_user=False)

        except Exception as e:
            # Manejo de errores
            if typing_indicator in self.messages_column.controls:
                self.messages_column.controls.remove(typing_indicator)
            self.add_chat_message("Lo siento, ocurrió un error inesperado.", is_user=False)

        finally:
            self.page.update()

    def create_typing_indicator(self) -> ft.Container:
        """Crea un indicador de escritura."""
        return ft.Container(
            content=ft.Row([
                ft.ProgressRing(width=16, height=16),
                ft.Text("El asistente está escribiendo...", italic=True, size=12)
            ], spacing=10),
            padding=10,
        )

    def add_chat_message(self, message: str, is_user: bool):
        """Añade un mensaje al chat."""
        message_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(
                        ft.icons.PERSON if is_user else ft.icons.SMART_TOY,
                        color=ft.colors.BLUE_GREY_700,
                        size=16,
                    ),
                    ft.Text(
                        "Tú" if is_user else "Asistente",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_GREY_700,
                    ),
                ], spacing=4),
                ft.Container(
                    content=ft.Text(
                        message,
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    bgcolor=ft.colors.WHITE,
                    border_radius=8,
                    padding=10,
                ),
            ]),
            margin=ft.margin.only(
                left=50 if is_user else 0,
                right=0 if is_user else 50,
                bottom=10,
            ),
        )

        self.messages_column.controls.append(message_container)
        self.page.update()