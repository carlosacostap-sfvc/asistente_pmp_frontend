import flet as ft
from typing import Optional, Callable
from src.models.question import Question
from src.models.quiz_session import QuizAnswer
from src.ui.components import create_title, create_container, create_button


class QuestionView:
    def __init__(
        self,
        on_answer_submitted: Callable,
    ):
        self.on_answer_submitted = on_answer_submitted
        self.page = None
        self.current_question = None
        self.selected_value = None

    def build(self, page: ft.Page, question: Question):
        self.page = page
        self.current_question = question
        self.selected_value = None

        # Obtener el número de pregunta actual
        question_number = len(page.quiz_session.answers) + 1

        # Configurar la página
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = ft.padding.only(top=20)
        page.clean()

        # Crear el RadioGroup y las opciones
        self.radio_group = ft.RadioGroup(
            content=ft.Column(
                [self._create_radio_option(i, option) for i, option in enumerate(question.options)],
                spacing=10,
            ),
            on_change=lambda e: self.handle_option_selected(e)
        )

        # Botón de verificar respuesta
        self.submit_button = create_button(
            text="Verificar Respuesta",
            on_click=self.handle_submit_answer,
            disabled=True,
            bgcolor=ft.colors.BLUE_200,
        )

        domain_display = question.domain.capitalize()
        content = ft.Column(
            controls=[
                create_title(f"Pregunta {question_number} (Dominio: {domain_display})"),
                ft.Text(
                    question.question_text,
                    size=16,
                    color=ft.colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                self.radio_group,
                self.submit_button,
            ],
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    def _create_radio_option(self, index: int, option) -> ft.Radio:
        """Crea una opción de radio con el formato adecuado."""
        return ft.Radio(
            value=str(index),
            label=f"{chr(65 + index)}) {option.text}",
            label_style=ft.TextStyle(
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_400,
                size=14,
            ),
        )

    def handle_option_selected(self, e):
        """Maneja la selección de una opción de respuesta."""
        self.selected_value = e.data
        self.submit_button.disabled = False
        self.submit_button.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.colors.BLUE_800,
            color=ft.colors.WHITE,
        )
        self.page.update()

    async def handle_submit_answer(self, e):
        """Maneja la verificación de la respuesta."""
        if self.current_question and self.selected_value:
            # Obtener la opción correcta
            correct_option = next(
                (i for i, opt in enumerate(self.current_question.options) if opt.is_correct),
                None
            )
            is_correct = int(self.selected_value) == correct_option

            # Registrar la respuesta en la sesión
            if hasattr(self.page, 'quiz_session'):
                self.page.quiz_session.add_answer(
                    QuizAnswer(
                        question_text=self.current_question.question_text,
                        selected_option=chr(65 + int(self.selected_value)),
                        correct_option=chr(65 + correct_option),
                        is_correct=is_correct,
                        domain=self.current_question.domain,
                        explanation=self.current_question.explanation
                    )
                )

            # Notificar que se ha enviado una respuesta
            await self.on_answer_submitted(
                e,
                self.current_question,
                chr(65 + int(self.selected_value)),
                is_correct
            )