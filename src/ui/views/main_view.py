import flet as ft
import random
from src.ui.components import create_title

class MainView:
    def __init__(self, on_practice):
        self.on_practice = on_practice
        self.page = None

    def build(self, page: ft.Page):
        self.page = page
        page.title = "Práctica para el examen PMP"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = ft.padding.only(top=20)
        page.clean()

        # Dropdown para selección de dominio
        domain_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("aleatorio", "Aleatorio"),
                ft.dropdown.Option("personas", "Personas"),
                ft.dropdown.Option("proceso", "Proceso"),
                ft.dropdown.Option("entorno", "Entorno de negocio"),
            ],
            value="aleatorio"
        )

        async def handle_start(e):
            selected_domain = domain_dropdown.value
            if selected_domain == "aleatorio":
                selected_domain = random.choice(["personas", "proceso", "entorno"])
            await self.on_practice(e, selected_domain)

        content = ft.Column(
            controls=[
                create_title("Práctica para el examen PMP"),
                create_title("Selecciona el dominio para la primera pregunta:", size=16),
                domain_dropdown,
                ft.ElevatedButton(
                    text="Iniciar",
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        padding=15,
                    ),
                    width=200,
                    on_click=handle_start
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        container = ft.Container(
            content=content,
            padding=50,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
            )
        )

        page.add(container)
        page.update()