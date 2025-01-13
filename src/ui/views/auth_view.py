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

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        title = create_title(
            "PMP Question Generator",
            color=ft.colors.BLUE_GREY_900  # Color más oscuro para el título
        )

        subtitle = ft.Text(
            "Inicia sesión para continuar",
            size=16,
            color=ft.colors.BLUE_GREY_900,  # Color más oscuro para el subtítulo
            weight=ft.FontWeight.W_500
        )

        # Campos de entrada
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            border_color=ft.colors.BLUE,
            helper_text="Introduce tu email",
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_900),  # Color más oscuro para la etiqueta
            text_style=ft.TextStyle(color=ft.colors.BLUE_GREY_900),  # Color más oscuro para el texto ingresado
            hint_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700),  # Color para el texto de ayuda
        )

        self.password_field = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            border_color=ft.colors.BLUE,
            helper_text="Introduce tu contraseña",
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_900),  # Color más oscuro para la etiqueta
            text_style=ft.TextStyle(color=ft.colors.BLUE_GREY_900),  # Color más oscuro para el texto ingresado
            hint_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700),  # Color para el texto de ayuda
        )

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

        def toggle_mode(e):
            self.is_signup_mode = not self.is_signup_mode
            self.submit_button.text = "Registrarse" if self.is_signup_mode else "Iniciar Sesión"
            self.toggle_button.text = "¿Ya tienes cuenta? Inicia sesión" if self.is_signup_mode else "¿No tienes cuenta? Regístrate"
            self.page.update()

        # Botones
        self.submit_button = create_button(
            text="Iniciar Sesión",
            on_click=handle_submit,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        self.toggle_button = ft.TextButton(
            text="¿No tienes cuenta? Regístrate",
            on_click=toggle_mode,
            style=ft.ButtonStyle(
                color=ft.colors.BLUE_GREY_900  # Color más oscuro para el texto del botón
            ),
        )

        content = ft.Column(
            controls=[
                title,
                subtitle,
                self.email_field,
                self.password_field,
                self.submit_button,
                self.toggle_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        container = create_container(content)
        page.add(container)
        page.update()

    async def handle_login(self, e):
        """Maneja el proceso de login."""
        try:
            from src.services.api_service import api_service
            from src.ui.components import show_loading, hide_loading

            # Mostrar indicador de carga
            show_loading(self.page)

            success, error = await api_service.login(
                self.email_field.value,
                self.password_field.value
            )

            # Ocultar indicador de carga
            hide_loading(self.page)

            if success:
                # Es importante esperar a que el callback se complete
                await self.on_login_success(e)
            else:
                show_error_message(self.page, f"Error al iniciar sesión: {error}")
        except Exception as ex:
            # Asegurar que se oculte el loading incluso si hay error
            hide_loading(self.page)
            show_error_message(self.page, f"Error inesperado: {str(ex)}")

    async def handle_signup(self, e):
        """Maneja el proceso de registro."""
        try:
            from src.services.api_service import api_service
            from src.ui.components import show_loading, hide_loading

            # Mostrar indicador de carga
            show_loading(self.page)

            success, error = await api_service.signup(
                self.email_field.value,
                self.password_field.value
            )

            # Ocultar indicador de carga
            hide_loading(self.page)

            if success:
                # Es importante esperar a que el callback se complete
                await self.on_signup_success(e)
            else:
                show_error_message(self.page, f"Error al registrarse: {error}")
        except Exception as ex:
            # Asegurar que se oculte el loading incluso si hay error
            hide_loading(self.page)
            show_error_message(self.page, f"Error inesperado: {str(ex)}")