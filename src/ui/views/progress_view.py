import flet as ft
from typing import Callable, List
from datetime import datetime
from src.ui.components import create_title, create_container, create_button
from src.services.api_service import api_service
from src.models.quiz_session import PracticeSession


class ProgressView:
    def __init__(self, on_return_home: Callable):
        self.on_return_home = on_return_home
        self.page = None
        self.sessions: List[PracticeSession] = []

    def create_stat_card(self, icon: str, title: str, value: str, description: str = None) -> ft.Container:
        """Crea una tarjeta de estadística con el nuevo diseño."""
        return ft.Container(
            content=ft.Row([
                # Contenido principal
                ft.Row([
                    # Ícono
                    ft.Container(
                        content=ft.Icon(icon, size=24, color=ft.colors.BLUE),
                        margin=ft.margin.only(right=15),
                    ),
                    # Textos
                    ft.Column([
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            value,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE,
                        ),
                        ft.Text(
                            description if description else "",
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

    def create_domain_card(self, icon: str, domain: str, stats: dict) -> ft.Container:
        """Crea una tarjeta de dominio con el nuevo diseño."""
        percentage = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=24, color=ft.colors.BLUE),
                        margin=ft.margin.only(right=15),
                    ),
                    ft.Column([
                        ft.Text(
                            domain.capitalize(),
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Row([
                            ft.Column([
                                ft.Text(
                                    f"Total: {stats['total']}",
                                    size=14,
                                    color=ft.colors.GREY_700,
                                ),
                                ft.Text(
                                    f"Correctas: {stats['correct']}",
                                    size=14,
                                    color=ft.colors.GREY_700,
                                ),
                            ]),
                            ft.Container(
                                content=ft.Text(
                                    f"{percentage:.1f}%",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.GREEN if percentage >= 70 else ft.colors.ORANGE if percentage >= 50 else ft.colors.RED,
                                ),
                                margin=ft.margin.only(left=20),
                            ),
                        ]),
                        ft.ProgressBar(
                            value=percentage / 100,
                            bgcolor=ft.colors.GREY_200,
                            color=ft.colors.GREEN if percentage >= 70 else ft.colors.ORANGE if percentage >= 50 else ft.colors.RED,
                            width=400,
                        ),
                    ],
                        spacing=5,
                    ),
                ], expand=True),
                ft.Icon(
                    ft.icons.ARROW_FORWARD_IOS,
                    size=20,
                    color=ft.colors.GREY_400,
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            ink=True,
        )

    def create_session_card(self, session: PracticeSession) -> ft.Container:
        """Crea una tarjeta de sesión con el nuevo diseño."""
        total_questions = (session.personas_total + session.proceso_total + session.entorno_total)
        total_correct = (session.personas_correct + session.proceso_correct + session.entorno_correct)
        percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.HISTORY_EDU, size=24, color=ft.colors.BLUE),
                        margin=ft.margin.only(right=15),
                    ),
                    ft.Column([
                        ft.Text(
                            f"Sesión del {session.start_time.strftime('%d/%m/%Y %H:%M')}",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLACK,
                        ),
                        ft.Row([
                            ft.Text(
                                f"Preguntas: {total_questions}",
                                size=14,
                                color=ft.colors.GREY_700,
                            ),
                            ft.Text(
                                f"Correctas: {total_correct}",
                                size=14,
                                color=ft.colors.GREY_700,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"{percentage:.1f}%",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.GREEN if percentage >= 70 else ft.colors.ORANGE if percentage >= 50 else ft.colors.RED,
                                ),
                                margin=ft.margin.only(left=20),
                            ),
                        ], spacing=20),
                    ],
                        spacing=5,
                    ),
                ], expand=True),
                ft.Icon(
                    ft.icons.ARROW_FORWARD_IOS,
                    size=20,
                    color=ft.colors.GREY_400,
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            ink=True,
        )

    def create_section_title(self, text: str) -> ft.Text:
        """Crea un título de sección."""
        return ft.Text(
            text,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK,
        )

    async def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.bgcolor = ft.colors.GREY_50

        # Cargar las sesiones del usuario
        await self.load_sessions()
        stats = self.calculate_stats()

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("Mi Progreso"),
            ft.Text(
                "Visualiza y analiza tu avance en la preparación para el examen PMP",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección de Resumen
            self.create_section_title("Resumen General"),
            ft.Row([
                self.create_stat_card(
                    ft.icons.QUIZ_OUTLINED,
                    "Total de Sesiones",
                    str(stats["total_sessions"]),
                ),
                self.create_stat_card(
                    ft.icons.QUESTION_ANSWER,
                    "Total de Preguntas",
                    str(stats["total_questions"]),
                ),
                self.create_stat_card(
                    ft.icons.ANALYTICS,
                    "Promedio General",
                    f"{stats['average_score']:.1f}%",
                ),
            ], wrap=True),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección de Dominios
            self.create_section_title("Progreso por Dominio"),
            self.create_domain_card(
                ft.icons.PEOPLE_OUTLINED,
                "Personas",
                stats["domain_stats"]["personas"]
            ),
            self.create_domain_card(
                ft.icons.ACCOUNT_TREE_OUTLINED,
                "Proceso",
                stats["domain_stats"]["proceso"]
            ),
            self.create_domain_card(
                ft.icons.BUSINESS_OUTLINED,
                "Entorno de Negocio",
                stats["domain_stats"]["entorno"]
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección de Historial
            self.create_section_title("Historial de Sesiones"),
            *[self.create_session_card(session) for session in self.sessions],

            # Botón de retorno
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=ft.colors.BLUE,
                        on_click=self.on_return_home,
                    ),
                    ft.Text(
                        "Volver al Inicio",
                        color=ft.colors.BLUE,
                        weight=ft.FontWeight.W_500,
                        size=16,
                    ),
                ]),
                on_click=self.on_return_home,
                ink=True,
            ),
        ])

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()

    async def load_sessions(self):
        """Carga las sesiones de práctica del usuario."""
        try:
            if api_service.current_user:
                self.sessions = await api_service.get_user_practice_sessions(
                    api_service.current_user.id
                )
        except Exception as e:
            print(f"Error cargando sesiones: {e}")
            self.sessions = []

    def calculate_stats(self):
        """Calcula estadísticas generales de las sesiones."""
        if not self.sessions:
            return {
                "total_sessions": 0,
                "total_questions": 0,
                "average_score": 0,
                "domain_stats": {
                    "personas": {"total": 0, "correct": 0},
                    "proceso": {"total": 0, "correct": 0},
                    "entorno": {"total": 0, "correct": 0}
                }
            }

        stats = {
            "total_sessions": len(self.sessions),
            "total_questions": 0,
            "total_correct": 0,
            "domain_stats": {
                "personas": {"total": 0, "correct": 0},
                "proceso": {"total": 0, "correct": 0},
                "entorno": {"total": 0, "correct": 0}
            }
        }

        for session in self.sessions:
            # Estadísticas por dominio
            stats["domain_stats"]["personas"]["total"] += session.personas_total
            stats["domain_stats"]["personas"]["correct"] += session.personas_correct
            stats["domain_stats"]["proceso"]["total"] += session.proceso_total
            stats["domain_stats"]["proceso"]["correct"] += session.proceso_correct
            stats["domain_stats"]["entorno"]["total"] += session.entorno_total
            stats["domain_stats"]["entorno"]["correct"] += session.entorno_correct

            # Totales generales
            total_session = (session.personas_total + session.proceso_total + session.entorno_total)
            correct_session = (session.personas_correct + session.proceso_correct + session.entorno_correct)

            stats["total_questions"] += total_session
            stats["total_correct"] += correct_session

        # Calcular porcentaje general
        stats["average_score"] = (stats["total_correct"] / stats["total_questions"] * 100) if stats[
                                                                                                  "total_questions"] > 0 else 0

        return stats