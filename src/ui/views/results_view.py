import flet as ft
from typing import Callable
from src.models.quiz_session import QuizSession
from src.ui.components import create_title, create_container, create_button


class ResultsView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.page = None

    def build(self, page: ft.Page, session: QuizSession):
        self.page = page
        page.clean()

        stats = session.get_stats_by_domain()

        # Crear estadísticas por dominio
        domain_results = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Dominio: {domain.capitalize()}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Total preguntas: {data['total']}", size=14),
                        ft.Text(f"Correctas: {data['correct']}", size=14),
                        ft.Text(
                            f"Porcentaje: {(data['correct'] / data['total'] * 100):.1f}%",
                            size=14
                        ),
                        ft.ProgressBar(
                            value=data['correct'] / data['total'],
                            width=200,
                            color=ft.colors.GREEN
                        )
                    ]),
                    padding=20,
                    bgcolor=ft.colors.BLUE_50,
                    border_radius=10,
                    margin=10,
                )
                for domain, data in stats.items()
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Lista detallada de respuestas
        answers_list = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pregunta {i + 1}: {answer.question_text}", size=14),
                        ft.Text(
                            f"Tu respuesta: {answer.selected_option}",
                            color=ft.colors.GREEN if answer.is_correct else ft.colors.RED
                        ),
                        ft.Text(f"Respuesta correcta: {answer.correct_option}"),
                        ft.Text(f"Explicación: {answer.explanation}", size=12, color=ft.colors.GREY_700),
                        ft.Divider()
                    ]),
                    padding=10
                )
                for i, answer in enumerate(session.answers)
            ],
            height=300,
            spacing=10
        )

        content = ft.Column(
            controls=[
                create_title("Resultados de la Práctica"),
                domain_results,
                ft.Divider(),
                ft.Text("Detalle de respuestas:", size=16, weight=ft.FontWeight.BOLD),
                answers_list,
                create_button(
                    text="Volver al inicio",
                    on_click=self.on_return_home,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container = create_container(content)
        page.add(container)
        page.update()