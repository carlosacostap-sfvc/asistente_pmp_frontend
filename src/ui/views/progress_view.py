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
            total_session = (session.personas_total + session.proceso_total +
                             session.entorno_total)
            correct_session = (session.personas_correct + session.proceso_correct +
                               session.entorno_correct)

            stats["total_questions"] += total_session
            stats["total_correct"] += correct_session

        # Calcular porcentaje general
        if stats["total_questions"] > 0:
            stats["average_score"] = (stats["total_correct"] /
                                      stats["total_questions"] * 100)
        else:
            stats["average_score"] = 0

        return stats

    def create_domain_progress(self, domain_name: str, stats: dict) -> ft.Container:
        """Crea una visualización del progreso por dominio."""
        domain_stats = stats["domain_stats"][domain_name]
        percentage = (domain_stats["correct"] / domain_stats["total"] * 100
                      if domain_stats["total"] > 0 else 0)

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    f"Dominio: {domain_name.capitalize()}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Preguntas: {domain_stats['total']}",
                    size=14,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Correctas: {domain_stats['correct']}",
                    size=14,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Porcentaje: {percentage:.1f}%",
                    size=14,
                    color=ft.colors.GREEN if percentage >= 70 else
                    ft.colors.ORANGE if percentage >= 50 else
                    ft.colors.RED,
                ),
                ft.ProgressBar(
                    value=percentage / 100,
                    bgcolor=ft.colors.GREY_300,
                    color=ft.colors.GREEN if percentage >= 70 else
                    ft.colors.ORANGE if percentage >= 50 else
                    ft.colors.RED,
                )
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_400),
        )

    def create_sessions_list(self) -> ft.ListView:
        """Crea una lista con el historial de sesiones."""
        sessions_list = ft.ListView(
            spacing=10,
            height=200,
            width=400,
        )

        for session in self.sessions:
            total_questions = (session.personas_total + session.proceso_total +
                               session.entorno_total)
            total_correct = (session.personas_correct + session.proceso_correct +
                             session.entorno_correct)
            percentage = (total_correct / total_questions * 100
                          if total_questions > 0 else 0)

            session_container = ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Fecha: {session.start_time.strftime('%d/%m/%Y %H:%M')}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                    ),
                    ft.Text(
                        f"Preguntas: {total_questions} | "
                        f"Correctas: {total_correct} | "
                        f"Porcentaje: {percentage:.1f}%",
                        size=14,
                        color=ft.colors.BLACK,
                    ),
                ]),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=5,
                border=ft.border.all(1, ft.colors.GREY_400),
            )
            sessions_list.controls.append(session_container)

        return sessions_list

    async def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO

        # Cargar las sesiones del usuario
        await self.load_sessions()
        stats = self.calculate_stats()

        # Crear resumen general
        summary = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Resumen General",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Total de sesiones: {stats['total_sessions']}",
                    size=16,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Total de preguntas: {stats['total_questions']}",
                    size=16,
                    color=ft.colors.BLACK,
                ),
                ft.Text(
                    f"Promedio general: {stats['average_score']:.1f}%",
                    size=16,
                    color=ft.colors.GREEN if stats['average_score'] >= 70 else
                    ft.colors.ORANGE if stats['average_score'] >= 50 else
                    ft.colors.RED,
                ),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_400),
        )

        # Crear progreso por dominio
        domains_progress = ft.Row(
            controls=[
                self.create_domain_progress("personas", stats),
                self.create_domain_progress("proceso", stats),
                self.create_domain_progress("entorno", stats),
            ],
            wrap=True,
            spacing=20,
        )

        # Crear historial de sesiones
        sessions_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Historial de Sesiones",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                self.create_sessions_list() if self.sessions else
                ft.Text("No hay sesiones registradas", color=ft.colors.BLACK),
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_400),
        )

        # Botón de retorno
        return_button = create_button(
            text="Volver al inicio",
            on_click=self.on_return_home,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        # Contenido principal
        content = ft.Column(
            controls=[
                create_title(f"Mi Progreso ({api_service.current_user.email})"),
                summary,
                ft.Divider(),
                ft.Text(
                    "Progreso por Dominio",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                domains_progress,
                ft.Divider(),
                sessions_container,
                return_button,
            ],
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()