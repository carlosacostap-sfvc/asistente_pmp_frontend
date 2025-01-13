# En ui/views/practice_intro_view.py
import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button

class PracticeIntroView:
    def __init__(self, on_start_practice: Callable):
        self.on_start_practice = on_start_practice
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Mejorar el dropdown con mejor estilo visual
        self.domain_dropdown = ft.Dropdown(
            width=300,  # Aumentar el ancho
            options=[
                ft.dropdown.Option("aleatorio", "Aleatorio"),
                ft.dropdown.Option("personas", "Personas"),
                ft.dropdown.Option("proceso", "Proceso"),
                ft.dropdown.Option("entorno", "Entorno de negocio"),
            ],
            value="aleatorio",
            text_size=16,  # Tamaño de texto más grande
            color=ft.colors.BLUE_GREY_900,  # Color del texto más oscuro
            bgcolor=ft.colors.WHITE,  # Fondo blanco
            border_color=ft.colors.BLUE_400,  # Borde azul
            border_width=2,  # Borde más grueso
            focused_border_color=ft.colors.BLUE,  # Color del borde cuando está enfocado
            focused_bgcolor=ft.colors.WHITE,  # Color de fondo cuando está enfocado
            content_padding=ft.padding.only(left=20, right=20, top=10, bottom=10),  # Más padding
        )

        async def handle_start(e):
            await self.on_start_practice(e, self.domain_dropdown.value)

        start_button = create_button(
            text="Comenzar Práctica",
            on_click=lambda e: self.page.loop.create_task(handle_start(e)),
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            width=300  # Mismo ancho que el dropdown
        )

        content = ft.Column(
            controls=[
                create_title("¡Bienvenido a una nueva sesión de práctica!"),
                ft.Text(
                    "Prepárate para poner a prueba tus conocimientos en gestión de proyectos.",
                    size=16,
                    color=ft.colors.BLUE_GREY_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Text(
                    "¿De qué dominio te gustaría que fuera tu primera pregunta?",
                    size=16,
                    color=ft.colors.BLUE_GREY_900,
                    weight=ft.FontWeight.W_500
                ),
                self.domain_dropdown,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                start_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Usar create_container sin el parámetro bgcolor ya que está incluido en la función
        container = create_container(content=content, padding=40)

        page.add(container)
        page.update()