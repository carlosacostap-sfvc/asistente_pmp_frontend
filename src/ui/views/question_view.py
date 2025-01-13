import flet as ft
import random
from typing import Optional, List, Callable
from datetime import datetime
from src.models.question import Question
from src.models.quiz_session import QuizAnswer
from src.ui.components import create_title, create_container, create_button


class QuestionView:
    def __init__(
            self,
            on_next_question: Callable,
            on_return_home: Callable,
            on_finish_practice: Callable,
    ):
        self.on_next_question = on_next_question
        self.on_return_home = on_return_home
        self.on_finish_practice = on_finish_practice
        self.current_question = None
        self.page = None
        self.selected_value = None
        self.answer_submitted = False

    def build(self, page: ft.Page, question: Question):
        self.page = page
        self.current_question = question
        self.answer_submitted = False
        self.selected_value = None

        # Obtener el número de pregunta actual
        question_number = len(page.quiz_session.answers) + 1

        # Configurar la página
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = ft.padding.only(top=20)
        page.clean()

        # Dropdown para selección de dominio siguiente
        self.domain_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("aleatorio", "Aleatorio"),
                ft.dropdown.Option("personas", "Personas"),
                ft.dropdown.Option("proceso", "Proceso"),
                ft.dropdown.Option("entorno", "Entorno de negocio"),
            ],
            value="aleatorio",
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            text_style=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.W_500)
        )

        # Crear el RadioGroup y las opciones
        self.radio_group = ft.RadioGroup(
            content=ft.Column(
                [
                    self._create_radio_option(i, option)
                    for i, option in enumerate(question.options)
                ],
                spacing=10,
            ),
            on_change=lambda e: self.handle_option_selected(e)
        )

        # Contenedor para la explicación (inicialmente oculto)
        self.explanation_container = ft.Container(
            visible=False,
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
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
        )

        # Contenedor para el resultado (inicialmente oculto)
        self.result_container = ft.Container(
            visible=False,
            content=None,
            padding=10,
            border_radius=8,
        )

        # Botones de acción
        # En el método build
        self.submit_button = create_button(
            text="Verificar Respuesta",
            on_click=self.handle_submit_answer,
            disabled=True,
            bgcolor=ft.colors.BLUE_200,  # Azul claro inicial
            color=ft.colors.WHITE,
        )

        self.next_button = create_button(
            text="Siguiente Pregunta",
            on_click=self.handle_next_question,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        )

        self.finish_button = create_button(
            text="Finalizar Práctica",
            on_click=self.handle_finish_practice,
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
        )

        # Crear contenedor para siguiente pregunta (inicialmente oculto)
        self.siguiente_pregunta_container = ft.Container(
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
                        self.domain_dropdown,
                        self.next_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
            ]),
            padding=ft.padding.all(20),
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
            visible=False  # Inicialmente oculto
        )

        # El botón de finalizar también debe estar oculto inicialmente
        self.finish_button.visible = False

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
                self.result_container,
                self.explanation_container,
                ft.Divider(),
                self.siguiente_pregunta_container,
                self.finish_button,
            ],
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    def _create_radio_option(self, index: int, option) -> ft.Radio:
        """Crea una opción de radio con el formato adecuado y mejor contraste."""
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
        """Maneja la selección de una opción de respuesta"""
        if not self.answer_submitted:
            self.selected_value = e.data
            # Habilitamos el botón y cambiamos a un azul más oscuro
            self.submit_button.disabled = False
            self.submit_button.style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.colors.BLUE_800,  # Azul más oscuro cuando está habilitado
                color=ft.colors.WHITE,
            )
            self.page.update()

    def handle_submit_answer(self, e):
        """Maneja la verificación de la respuesta"""
        if self.current_question and self.selected_value:
            self.answer_submitted = True

            # Obtener la opción correcta
            correct_option = next(
                (i for i, opt in enumerate(self.current_question.options) if opt.is_correct),
                None
            )
            is_correct = int(self.selected_value) == correct_option

            # Deshabilitar las opciones de respuesta y ajustar colores
            self.radio_group.disabled = True

            # Ajustar cada radio button y su texto
            for radio in self.radio_group.content.controls:
                radio = radio if isinstance(radio, ft.Radio) else radio.content

                # Aplicar estilos al radio button
                radio.value = radio.value
                radio.disabled = True
                radio.fill_color = ft.colors.GREY
                radio.inactive_color = ft.colors.GREY_400

                # Forzar el color del texto
                current_label = radio.label
                radio.label = current_label
                radio.label_style = ft.TextStyle(
                    color=ft.colors.BLACK54,
                    weight=ft.FontWeight.W_400,
                    size=14,
                )

            # 2. Deshabilitar el botón de verificar respuesta
            self.submit_button.disabled = True

            # 3. Mostrar el resultado (correcto/incorrecto)
            self.result_container.content = ft.Row(
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
            )
            self.result_container.visible = True

            # 4. Mostrar la explicación con texto negro
            self.explanation_container.content = ft.Column([
                ft.Text(
                    "Explicación:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK
                ),
                ft.Text(
                    self.current_question.explanation,
                    size=14,
                    color=ft.colors.BLACK
                )
            ])
            self.explanation_container.visible = True

            # 5. Habilitar y mostrar en negro los labels de nueva pregunta
            self.siguiente_pregunta_container.visible = True
            self.finish_button.visible = True

            # 6. Habilitar selector de dominio con letras negras
            self.domain_dropdown.disabled = False
            self.domain_dropdown.label_style = ft.TextStyle(
                color=ft.colors.BLACK,
            )
            self.domain_dropdown.text_style = ft.TextStyle(
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_500
            )

            # 7. Habilitar botón de siguiente pregunta (verde con letras blancas)
            self.next_button.disabled = False
            self.next_button.style = ft.ButtonStyle(
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10)
            )

            # 8. Habilitar botón de finalizar (rojo con letras blancas)
            self.finish_button.disabled = False
            self.finish_button.style = ft.ButtonStyle(
                bgcolor=ft.colors.RED,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10)
            )

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

            # Actualizar la página
            self.page.update()

    async def handle_next_question(self, e):
        """Maneja la generación de la siguiente pregunta"""
        selected_domain = self.domain_dropdown.value
        if selected_domain == "aleatorio":
            selected_domain = random.choice(["personas", "proceso", "entorno"])
        await self.on_next_question(e, selected_domain)

    async def handle_finish_practice(self, e):
        """Maneja el fin de la práctica"""
        await self.on_finish_practice(e)