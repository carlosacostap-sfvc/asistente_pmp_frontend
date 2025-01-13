import flet as ft
from typing import Callable, Optional
from src.models.question import Question
from src.ui.components import create_title, create_container, create_button

class AnswerView:
    def __init__(
        self,
        on_next_question: Callable,
        on_finish_practice: Callable,
    ):
        self.on_next_question = on_next_question
        self.on_finish_practice = on_finish_practice
        self.page = None

    def build(self, page: ft.Page, question: Question, selected_answer: str, is_correct: bool):
        """Construye la vista de respuesta con la explicación."""
        self.page = page
        page.clean()

        # Obtener letra de la respuesta correcta e índices
        correct_option_index = next(
            (i for i, opt in enumerate(question.options) if opt.is_correct),
            None
        )
        correct_option = chr(65 + correct_option_index) if correct_option_index is not None else "?"
        selected_index = ord(selected_answer) - 65

        # Contenedor de resultado (Correcto/Incorrecto)
        result_container = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.icons.CHECK_CIRCLE if is_correct else ft.icons.ERROR,
                        color=ft.colors.GREEN if is_correct else ft.colors.RED,
                        size=24
                    ),
                    ft.Text(
                        "¡Correcto!" if is_correct else "Incorrecto",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREEN if is_correct else ft.colors.RED
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            padding=10,
            border_radius=8,
        )

        # Contenedor de la pregunta y opciones
        question_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    question.question_text,
                    size=16,
                    color=ft.colors.BLACK,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                # Lista de opciones
                *[self._create_option_display(
                    i,
                    opt.text,
                    i == selected_index,  # Es la seleccionada
                    i == correct_option_index  # Es la correcta
                ) for i, opt in enumerate(question.options)]
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.BLUE_100)
        )

        # Contenedor de explicación
        explanation_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Explicación:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK
                ),
                ft.Text(
                    question.explanation,
                    size=14,
                    color=ft.colors.BLACK
                )
            ]),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
        )

        # Dropdown para siguiente pregunta
        domain_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("aleatorio", "Aleatorio"),
                ft.dropdown.Option("personas", "Personas"),
                ft.dropdown.Option("proceso", "Proceso"),
                ft.dropdown.Option("entorno", "Entorno de negocio"),
            ],
            value="aleatorio",
            text_style=ft.TextStyle(
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_500,
                size=14,
            ),
            label_style=ft.TextStyle(
                color=ft.colors.BLACK,
            ),
            focused_border_color=ft.colors.BLUE,
            focused_bgcolor=ft.colors.WHITE,
            border_color=ft.colors.GREY_400,
            bgcolor=ft.colors.WHITE,
        )

        # Botones de acción
        next_button = create_button(
            text="Siguiente Pregunta",
            on_click=lambda e: self.handle_next_question(e, domain_dropdown.value),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        )

        finish_button = create_button(
            text="Finalizar Práctica",
            on_click=self.handle_finish_practice,
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
        )

        # Contenedor para siguiente pregunta
        next_question_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Siguiente pregunta:",
                    size=14,
                    color=ft.colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Dominio:",
                            size=14,
                            color=ft.colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        domain_dropdown,
                        next_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
            ]),
            padding=ft.padding.all(20),
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
        )

        # Construir contenido principal
        content = ft.Column(
            controls=[
                create_title(f"Respuesta Pregunta {len(page.quiz_session.answers)}"),
                result_container,
                question_container,
                explanation_container,
                ft.Divider(),
                next_question_container,
                finish_button,
            ],
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    def _create_option_display(self, index: int, text: str, is_selected: bool, is_correct: bool) -> ft.Container:
        """Crea una representación visual de una opción de respuesta."""
        background_color = ft.colors.WHITE
        border_color = ft.colors.GREY_300
        text_color = ft.colors.BLACK

        if is_selected and is_correct:
            background_color = ft.colors.GREEN_50
            border_color = ft.colors.GREEN
            text_color = ft.colors.GREEN_900
        elif is_selected and not is_correct:
            background_color = ft.colors.RED_50
            border_color = ft.colors.RED
            text_color = ft.colors.RED_900
        elif is_correct:
            background_color = ft.colors.GREEN_50
            border_color = ft.colors.GREEN
            text_color = ft.colors.GREEN_900

        return ft.Container(
            content=ft.Text(
                f"{chr(65 + index)}) {text}",
                color=text_color,
                size=14,
                weight=ft.FontWeight.W_500 if (is_selected or is_correct) else ft.FontWeight.NORMAL,
            ),
            padding=10,
            bgcolor=background_color,
            border_radius=5,
            border=ft.border.all(1, border_color),
            margin=ft.margin.only(bottom=5),
        )

    async def handle_next_question(self, e, domain: str):
        """Maneja la navegación a la siguiente pregunta."""
        await self.on_next_question(e, domain)

    async def handle_finish_practice(self, e):
        """Maneja la finalización de la práctica."""
        await self.on_finish_practice(e)