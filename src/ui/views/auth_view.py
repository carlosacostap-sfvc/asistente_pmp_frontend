import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button, show_error_message


class AuthView:
    def __init__(
            self,
            on_login_success: Callable,
            on_signup_success: Callable
    ):
        self.on_login_success = on_login_success
        self.on_signup_success = on_signup_success
        self.page = None
        self.is_signup_mode = False

    def create_auth_card(self, icon: str, title: str, description: str, fields: list) -> ft.Container:
        """Crea una tarjeta de autenticación con el nuevo diseño."""
        return ft.Container(
            content=ft.Column([
                # Encabezado con icono y título
                ft.Row([
                    ft.Icon(icon, size=24, color=ft.colors.BLUE),
                    ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK,
                    ),
                ], alignment=ft.MainAxisAlignment.START, spacing=10),

                # Descripción
                ft.Text(
                    description,
                    size=14,
                    color=ft.colors.GREY_700,
                    weight=ft.FontWeight.W_400
                ),

                # Campos de entrada
                ft.Column(fields, spacing=10),

            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_200),
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

    def create_input_field(self, label: str, icon: str, password: bool = False) -> ft.TextField:
        """Crea un campo de entrada estilizado."""
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            width=400,
            height=50,
            border_radius=8,
            password=password,
            can_reveal_password=password,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            focused_bgcolor=ft.colors.WHITE,
            bgcolor=ft.colors.WHITE,
            text_size=14,
            text_style=ft.TextStyle(
                color=ft.colors.BLACK,
                size=14,
                weight=ft.FontWeight.W_500
            ),
            label_style=ft.TextStyle(
                color=ft.colors.GREY_800,
                size=14,
                weight=ft.FontWeight.W_500
            ),
        )

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.bgcolor = ft.colors.GREY_50
        page.padding = 40
        page.scroll = ft.ScrollMode.AUTO

        # Campos de entrada
        self.email_field = self.create_input_field("Email", ft.icons.EMAIL)
        self.password_field = self.create_input_field("Contraseña", ft.icons.LOCK, password=True)

        async def handle_submit(e):
            email = self.email_field.value
            password = self.password_field.value

            if not email or not password:
                show_error_message(self.page, "Por favor, completa todos los campos")
                return

            if self.is_signup_mode:
                await self.handle_signup(e)
            else:
                await self.handle_login(e)

        # Botón principal
        self.submit_button = create_button(
            text="Iniciar Sesión",
            on_click=handle_submit,
            width=400,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        # Botón para cambiar modo
        self.toggle_button = ft.TextButton(
            text="¿No tienes cuenta? Regístrate",
            on_click=lambda e: self.toggle_mode(),
            style=ft.ButtonStyle(
                color=ft.colors.BLUE_800,
            ),
        )

        # Crear tarjetas de autenticación
        auth_card = self.create_auth_card(
            icon=ft.icons.PERSON,
            title="Acceso a tu cuenta",
            description="Ingresa tus credenciales para continuar" if not self.is_signup_mode
            else "Crea una nueva cuenta para comenzar",
            fields=[
                self.email_field,
                self.password_field,
                self.submit_button,
                self.toggle_button,
            ]
        )

        # Crear tarjeta de beneficios
        benefits_card = self.create_auth_card(
            icon=ft.icons.STAR,
            title="Beneficios de la plataforma",
            description="Al registrarte tendrás acceso a:",
            fields=[
                self.create_benefit_row(ft.icons.QUIZ, "Preguntas de práctica actualizadas"),
                self.create_benefit_row(ft.icons.CHAT, "Chat con IA para resolver dudas"),
                self.create_benefit_row(ft.icons.TRENDING_UP, "Seguimiento de tu progreso"),
                self.create_benefit_row(ft.icons.SCHOOL, "Recursos educativos premium"),
            ]
        )

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("PMP Question Generator"),
            ft.Text(
                "Tu plataforma de preparación para la certificación PMP",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Contenedor principal con las dos columnas
            ft.Row([
                # Columna izquierda: formulario de login
                ft.Column([auth_card], expand=True),

                # Columna derecha: beneficios
                ft.Column([benefits_card], expand=True),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40,
            )
        ])

        # Contenedor principal
        container = create_container(content)
        page.add(container)
        page.update()

    def create_benefit_row(self, icon: str, text: str) -> ft.Row:
        """Crea una fila con icono y texto para los beneficios."""
        return ft.Row([
            ft.Icon(icon, size=20, color=ft.colors.BLUE_400),
            ft.Text(
                text,
                size=14,
                color=ft.colors.GREY_800,
                weight=ft.FontWeight.W_400
            )
        ], spacing=10)

    def toggle_mode(self):
        """Alterna entre modo login y registro."""
        self.is_signup_mode = not self.is_signup_mode
        self.submit_button.text = "Registrarse" if self.is_signup_mode else "Iniciar Sesión"
        self.toggle_button.text = "¿Ya tienes cuenta? Inicia sesión" if self.is_signup_mode else "¿No tienes cuenta? Regístrate"
        self.page.update()

    async def handle_login(self, e):
        """Maneja el proceso de login."""
        try:
            from src.services.api_service import api_service
            from src.ui.components import show_loading, hide_loading

            show_loading(self.page)
            success, error = await api_service.login(
                self.email_field.value,
                self.password_field.value
            )
            hide_loading(self.page)

            if success:
                await self.on_login_success(e)
            else:
                show_error_message(self.page, f"Error al iniciar sesión: {error}")
        except Exception as ex:
            hide_loading(self.page)
            show_error_message(self.page, f"Error inesperado: {str(ex)}")

    async def handle_signup(self, e):
        """Maneja el proceso de registro."""
        try:
            from src.services.api_service import api_service
            from src.ui.components import show_loading, hide_loading

            show_loading(self.page)
            success, error = await api_service.signup(
                self.email_field.value,
                self.password_field.value
            )
            hide_loading(self.page)

            if success:
                await self.on_signup_success(e)
            else:
                show_error_message(self.page, f"Error al registrarse: {error}")
        except Exception as ex:
            hide_loading(self.page)
            show_error_message(self.page, f"Error inesperado: {str(ex)}")