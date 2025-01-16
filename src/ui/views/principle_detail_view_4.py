import flet as ft
from typing import Callable, Optional
from src.ui.components import create_title, create_container, create_button
from src.models.quiz_session import QuizAnswer


class PrincipleDetailView4:
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
            "Completar todas las tareas planificadas dentro del presupuesto",
            "Entregar el proyecto antes de la fecha límite",
            "Maximizar la entrega de valor al negocio y los stakeholders",
            "Documentar todos los entregables del proyecto"
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
                    "¿Cuál es el objetivo principal al enfocarse en el valor en la gestión de proyectos según el PMBOK 7?",
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
                    "Consulta tus dudas sobre el Principio 4: Enfocarse en el valor",
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
            create_title("Principio 4: Enfocarse en el valor"),
            ft.Text(
                "Prioriza la entrega de beneficios y la creación de valor para el negocio",
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
                    "Beneficios del Negocio",
                    "Identifica y prioriza las iniciativas que generan el mayor valor para la organización y los stakeholders."
                ),
                self.create_concept_card(
                    "Medición del Valor",
                    "Establece métricas claras para evaluar y monitorear la creación de valor a lo largo del proyecto."
                ),
            ], wrap=True),
            self.create_concept_card(
                "Alineación Estratégica",
                "Asegura que las decisiones y entregables del proyecto estén alineados con los objetivos estratégicos."
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
                        "Valor del negocio",
                        "ROI",
                        "Beneficios",
                        "Métricas",
                        "Priorización",
                        "Estrategia",
                        "Resultados"
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
                        "• El valor no siempre es financiero, puede incluir beneficios intangibles.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• La entrega temprana de valor es preferible a la entrega al final del proyecto.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• Las decisiones deben basarse en la maximización del valor para los stakeholders.",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        "• El valor debe ser medible y estar alineado con los objetivos estratégicos.",
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
                    "La respuesta correcta es C) Maximizar la entrega de valor al negocio y los stakeholders.\n\n"
                    "El PMBOK 7 enfatiza que el objetivo principal es la creación de valor para el negocio y los "
                    "stakeholders. Aunque completar tareas, cumplir plazos y documentar son importantes, son medios "
                    "para alcanzar el fin principal que es la generación de valor. El éxito del proyecto se mide "
                    "principalmente por el valor que aporta a la organización y sus interesados."
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
        self.messages_column.controls.append(typing_indicator)
        self.page.update()

        try:
            # Preparar el prompt con contexto del principio
            context_prompt = """
            Estás ayudando con dudas sobre el Principio 4 del PMBOK 7: Enfocarse en el valor.
            Este principio trata sobre la priorización de la entrega de beneficios y la creación de valor para el negocio.
            Conceptos clave incluyen: beneficios del negocio, medición del valor y alineación estratégica.
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