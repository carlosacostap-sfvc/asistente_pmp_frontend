import flet as ft
from datetime import datetime
from typing import Optional
from src.models.question import Question
from src.models.quiz_session import QuizSession
from src.services.api_service import api_service
from src.ui.views.auth_view import AuthView
from src.ui.views.educational_resources_view import EducationalResourcesView
from src.ui.views.main_view import MainView
from src.ui.views.question_view import QuestionView
from src.ui.views.results_view import ResultsView
from src.ui.views.selection_view import SelectionView
from src.ui.views.chat_view import ChatView
from src.ui.views.practice_intro_view import PracticeIntroView
from src.ui.views.answer_view import AnswerView
from src.ui.components import show_loading, hide_loading, show_error_message
from src.ui.views.progress_view import ProgressView
from src.ui.views.principles_view import PrinciplesView
from src.ui.views.principle_detail_view import PrincipleDetailView


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
        self.selection_view = SelectionView(
            on_practice_selected=self.handle_practice_selected,
            on_chat_selected=self.show_chat_view,
            on_progress_selected=self.show_progress_view,
            on_educational_resources_selected=self.show_educational_resources_view,
            on_logout=self.handle_logout
        )
        self.progress_view = ProgressView(
            on_return_home=self.show_selection_view
        )
        self.main_view = MainView(
            on_practice=self.handle_practice
        )
        self.question_view = QuestionView(
            on_answer_submitted=self.handle_answer_submitted
        )
        self.answer_view = AnswerView(
            on_next_question=self.handle_next_question,
            on_finish_practice=self.handle_finish_practice
        )
        self.results_view = ResultsView(
            on_return_home=self.show_selection_view
        )
        self.chat_view = ChatView(
            on_return_home=self.show_selection_view
        )
        self.practice_intro_view = PracticeIntroView(
            on_start_practice=self.handle_practice
        )
        self.principle_detail_view = PrincipleDetailView(
            on_return_to_principles=self.show_principles_view
        )
        self.principles_view = PrinciplesView(
            on_return_home=self.show_selection_view,
            on_principle_detail=self.show_principle_detail
        )
        self.educational_resources_view = EducationalResourcesView(
            on_return_home=self.show_selection_view,
            on_principles_selected=self.show_principles_view
        )

    def show_main_view(self, page: Optional[ft.Page] = None):
        """Muestra la vista principal o la vista de autenticación según corresponda."""
        if page is None and hasattr(self, 'page'):
            page = self.page
        elif isinstance(page, ft.Page):
            self.page = page
        elif hasattr(page, 'page'):
            self.page = page.page
            page = self.page
        else:
            raise ValueError("No se pudo obtener una referencia válida a la página")

        if not api_service.current_user:
            self.auth_view.build(page)
            return

        # Si está autenticado, muestra la vista de selección
        self.show_selection_view(page)

    def show_selection_view(self, page: Optional[ft.Page] = None):
        """Muestra la vista de selección entre chat y práctica."""
        if isinstance(page, ft.Page):
            self.page = page
        elif hasattr(page, 'page'):
            self.page = page.page
            page = self.page

        self.quiz_session = None
        hide_loading(page)
        self.selection_view.build(page)

    def show_chat_view(self, e):
        """Muestra la vista de chat."""
        page = e.page if hasattr(e, 'page') else self.page
        hide_loading(page)
        self.chat_view.build(page)

    def show_progress_view(self, e):
        """Muestra la vista de progreso."""
        page = e.page if hasattr(e, 'page') else self.page
        hide_loading(page)
        page.loop.create_task(self.progress_view.build(page))

    def show_educational_resources_view(self, e):
        """Muestra la vista de recursos educativos."""
        page = e.page if hasattr(e, 'page') else self.page
        self.educational_resources_view.build(page)

    def show_principles_view(self, e):
        """Muestra la vista de principios."""
        page = e.page if hasattr(e, 'page') else self.page
        self.principles_view.build(page)

    def show_principle_detail(self, e, principle_number: int):
        """Muestra la vista detallada de un principio específico."""
        page = e.page if hasattr(e, 'page') else self.page
        self.principle_detail_view.build(page)

    async def handle_login_success(self, e):
        """Maneja el evento de login exitoso."""
        self.show_selection_view(e)

    async def handle_signup_success(self, e):
        """Maneja el evento de registro exitoso."""
        self.show_selection_view(e)

    async def handle_logout(self, e):
        """Maneja el evento de cerrar sesión."""
        api_service.logout()
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

            # Iniciar nueva sesión si no existe
            if not hasattr(page, 'quiz_session'):
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

    async def handle_answer_submitted(self, e, question: Question, selected_answer: str, is_correct: bool):
        """Maneja cuando se envía una respuesta, mostrando la vista de respuesta."""
        self.answer_view.build(e.page, question, selected_answer, is_correct)

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

    async def handle_practice_selected(self, e):
        """Maneja la selección de práctica mostrando la vista de introducción"""
        self.practice_intro_view.build(e.page)