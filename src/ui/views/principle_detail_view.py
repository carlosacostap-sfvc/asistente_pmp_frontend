import flet as ft
from typing import Callable, Optional
from src.ui.components import create_title, create_container, create_button
from src.models.quiz_session import QuizAnswer


class PrincipleDetailView:
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
            auto_scroll=True  # Añadir auto-scroll
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
            "Remover inmediatamente al miembro del equipo del proyecto",
            "Documentar la situación y reportarla siguiendo los canales apropiados",
            "Confrontar al miembro del equipo en la próxima reunión de equipo",
            "Ignorar la situación si no impacta significativamente al proyecto"
        ]

        radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(
                    value=str(i),
                    label=f"{chr(65)}) {opt}" if i == 0 else
                    f"{chr(65 + i)}) {opt}",
                    label_style=ft.TextStyle(  # Añadir el estilo para el texto del label
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
                    "Durante la ejecución de un proyecto, descubres que un miembro clave del equipo está utilizando recursos del proyecto para beneficio personal. ¿Cuál debería ser tu primera acción como Project Manager?",
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
                    "Chat de Asistencia",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE,
                ),
                ft.Text(
                    "Consulta tus dudas sobre el Principio 1: Ser un administrador diligente",
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
            create_title("Principio 1: Ser un administrador diligente"),
            ft.Text(
                "Demuestra comportamiento ético y responsable en la gestión de proyectos",
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
                    "Responsabilidad Ética",
                    "Toma decisiones basadas en estándares éticos y profesionales, considerando el impacto en todos los interesados."
                ),
                self.create_concept_card(
                    "Gestión de Recursos",
                    "Administra recursos del proyecto (humanos, materiales, financieros) de manera eficiente y responsable."
                ),
            ], wrap=True),
            self.create_concept_card(
                "Transparencia",
                "Mantiene comunicación abierta y honesta sobre el estado del proyecto, riesgos y desafíos."
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
                        "Integridad",
                        "Responsabilidad",
                        "Transparencia",
                        "Conflicto de intereses",
                        "Código de conducta",
                        "Cumplimiento",
                        "Rendición de cuentas"
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
                        "• En preguntas sobre conflictos éticos, la respuesta correcta generalmente prioriza la transparencia y la comunicación.",
                        size=14,
                        color=ft.colors.BLACK,  # Añadir el color negro explícitamente
                    ),
                    ft.Text(
                        "• Recuerda que el Project Manager debe ser proactivo en identificar y abordar problemas éticos.",
                        size=14,
                        color=ft.colors.BLACK,  # Añadir el color negro explícitamente
                    ),
                    ft.Text(
                        "• La integridad del proyecto siempre debe mantenerse, incluso bajo presión de plazos o costos.",
                        size=14,
                        color=ft.colors.BLACK,  # Añadir el color negro explícitamente
                    ),
                    ft.Text(
                        "• Las decisiones deben considerar el beneficio de todos los stakeholders, no solo del sponsor.",
                        size=14,
                        color=ft.colors.BLACK,  # Añadir el color negro explícitamente
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
                    "La respuesta correcta es B) Documentar la situación y reportarla siguiendo los canales apropiados.\n\n"
                    "Como administrador diligente, es importante seguir los procedimientos establecidos y mantener "
                    "la documentación apropiada. Remover inmediatamente al miembro sería prematuro, confrontarlo "
                    "en una reunión podría ser contraproducente, e ignorar la situación sería poco ético."
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
        self.chat_messages_container.content.controls.append(typing_indicator)
        self.page.update()

        try:
            # Preparar el prompt con contexto del principio
            context_prompt = """
            Estás ayudando con dudas sobre el Principio 1 del PMBOK 7: Ser un administrador diligente.
            Este principio trata sobre demostrar comportamiento ético y responsable en la gestión de proyectos.
            Conceptos clave incluyen: responsabilidad ética, gestión de recursos y transparencia.
            La consulta del usuario debe ser respondida en este contexto.
            """

            from src.services.chat_service import chat_service
            response = await chat_service.send_message(
                f"{context_prompt}\n\nPregunta del usuario: {message}"
            )

            # Remover indicador de escritura
            if typing_indicator in self.chat_messages_container.content.controls:
                self.chat_messages_container.content.controls.remove(typing_indicator)

            # Mostrar respuesta
            if response.startswith("Error"):
                self.add_chat_message("Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.",
                                      is_user=False)
            else:
                self.add_chat_message(response, is_user=False)

        except Exception as e:
            # Manejo de errores
            if typing_indicator in self.chat_messages_container.content.controls:
                self.chat_messages_container.content.controls.remove(typing_indicator)
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

        # Añadir el mensaje a la column en lugar del container
        self.messages_column.controls.append(message_container)
        # La actualización de la página causará que auto_scroll funcione
        self.page.update()