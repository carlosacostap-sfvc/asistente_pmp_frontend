import flet as ft
from datetime import datetime
from typing import Optional
from src.models.question import Question
from src.models.quiz_session import QuizSession
from src.services.api_service import api_service
from src.ui.views.auth_view import AuthView
from src.ui.views.main_view import MainView
from src.ui.views.question_view import QuestionView
from src.ui.views.results_view import ResultsView
from src.ui.components import show_loading, hide_loading, show_error_message


class PMPQuizApp:
    def __init__(self):
        self.current_question: Optional[Question] = None
        self.page: Optional[ft.Page] = None
        self.quiz_session: Optional[QuizSession] = None

        # Initialize views
        self.auth_view = AuthView(
            on_login_success=self.handle_login_success,
            on_signup_success=self.handle_signup_success
        )
        self.main_view = MainView(
            on_practice=self.handle_practice
        )
        self.question_view = QuestionView(
            on_next_question=self.handle_next_question,
            on_return_home=self.show_main_view,
            on_finish_practice=self.handle_finish_practice
        )
        self.results_view = ResultsView(
            on_return_home=self.show_main_view
        )

    def show_main_view(self, page: Optional[ft.Page] = None):
        """Muestra la vista principal o la vista de autenticación según corresponda."""
        if page is None and hasattr(self, 'page'):
            page = self.page
        elif isinstance(page, ft.Page):
            self.page = page
        elif hasattr(page, 'page'):  # Si es un evento
            self.page = page.page
            page = self.page
        else:
            raise ValueError("No se pudo obtener una referencia válida a la página")

        if not api_service.current_user:
            self.auth_view.build(page)
            return

        # Si está autenticado, muestra la vista principal
        self.quiz_session = None
        hide_loading(page)
        self.main_view.build(page)

    async def handle_login_success(self, e):
        """Maneja el evento de login exitoso."""
        self.show_main_view(e)

    async def handle_signup_success(self, e):
        """Maneja el evento de registro exitoso."""
        self.show_main_view(e)

    async def handle_practice(self, e, domain: str):
        """Maneja la selección de práctica por dominio."""
        page = e.page
        show_loading(page)

        try:
            # Verificar autenticación
            if not api_service.current_user:
                self.show_main_view(page)
                return

            # Iniciar nueva sesión
            self.quiz_session = QuizSession(
                start_time=datetime.now(),
                answers=[]
            )
            page.quiz_session = self.quiz_session

            # Obtener primera pregunta
            question = await api_service.get_single_question(domain)
            if question:
                self.current_question = question
                hide_loading(page)
                self.question_view.build(page, self.current_question)
            else:
                show_error_message(page, "Error al obtener la pregunta")
        except Exception as e:
            show_error_message(page, f"Error: {str(e)}")
        finally:
            hide_loading(page)

    async def handle_next_question(self, e, domain: str):
        """Maneja el evento de siguiente pregunta."""
        page = e.page
        show_loading(page)

        try:
            # Verificar autenticación
            if not api_service.current_user:
                self.show_main_view(page)
                return

            question = await api_service.get_single_question(domain)
            if question:
                self.current_question = question
                hide_loading(page)
                self.question_view.build(page, self.current_question)
            else:
                show_error_message(page, "Error al obtener la siguiente pregunta")
        except Exception as e:
            show_error_message(page, f"Error: {str(e)}")
        finally:
            hide_loading(page)

    async def handle_finish_practice(self, e):
        """Maneja el evento de finalizar práctica."""
        page = e.page

        # Verificar autenticación
        if not api_service.current_user:
            self.show_main_view(page)
            return

        if self.quiz_session and self.quiz_session.answers:
            show_loading(page)
            try:
                # Guardar la sesión en la base de datos
                success = await api_service.save_practice_session(self.quiz_session)
                if not success:
                    show_error_message(page, "Error al guardar los resultados de la práctica")
            except Exception as e:
                show_error_message(page, f"Error: {str(e)}")
            finally:
                hide_loading(page)

            # Mostrar los resultados
            self.results_view.build(page, self.quiz_session)
        else:
            show_error_message(page, "No hay respuestas registradas para mostrar resultados")