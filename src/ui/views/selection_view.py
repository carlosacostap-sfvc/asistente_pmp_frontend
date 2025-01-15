import flet as ft
from src.ui.components import create_title, create_container, create_button

class SelectionView:
    def __init__(
        self,
        on_practice_selected,
        on_chat_selected,
        on_progress_selected,
        on_educational_resources_selected,
        on_logout
    ):
        self.on_practice_selected = on_practice_selected
        self.on_chat_selected = on_chat_selected
        self.on_progress_selected = on_progress_selected
        self.on_educational_resources_selected = on_educational_resources_selected
        self.on_logout = on_logout
        self.page = None

    def create_option_card(self, icon: str, title: str, description: str, on_click) -> ft.Container:
        """Crea una tarjeta de opción con el nuevo diseño."""
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
                            description,
                            size=14,
                            color=ft.colors.GREY_700,
                            width=400,
                        ),
                    ],
                    spacing=5,
                    ),
                ], expand=True),
                # Flecha derecha
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
            on_click=on_click,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

    def create_section_title(self, text: str) -> ft.Text:
        """Crea un título de sección."""
        return ft.Text(
            text,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK,
        )

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.bgcolor = ft.colors.GREY_50

        # Contenido principal
        content = ft.Column([
            # Título y descripción
            create_title("PMP Question Generator"),
            ft.Text(
                "Selecciona una opción para comenzar tu preparación",
                size=16,
                color=ft.colors.GREY_700,
                weight=ft.FontWeight.W_500,
            ),
            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección Práctica y Aprendizaje
            self.create_section_title("Práctica y Aprendizaje"),
            self.create_option_card(
                ft.icons.QUIZ_OUTLINED,
                "Práctica PMP",
                "Pon a prueba tus conocimientos con preguntas de práctica",
                lambda e: self.page.loop.create_task(self.handle_practice(e))
            ),
            self.create_option_card(
                ft.icons.CHAT_OUTLINED,
                "Chat con GPT",
                "Resuelve tus dudas con nuestro asistente virtual",
                self.handle_chat
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección Recursos y Seguimiento
            self.create_section_title("Recursos y Seguimiento"),
            self.create_option_card(
                ft.icons.TRENDING_UP,
                "Mi Progreso",
                "Visualiza y analiza tu avance en la preparación",
                self.handle_progress
            ),
            self.create_option_card(
                ft.icons.SCHOOL_OUTLINED,
                "Recursos Educativos",
                "Accede a material de estudio y guías de preparación",
                self.handle_educational_resources
            ),

            ft.Divider(height=30, color=ft.colors.GREY_300),

            # Sección Cuenta
            self.create_section_title("Cuenta"),
            self.create_option_card(
                ft.icons.LOGOUT,
                "Cerrar Sesión",
                "Finaliza tu sesión actual",
                lambda e: self.page.loop.create_task(self.handle_logout(e))
            ),
        ])

        # Contenedor principal con sombra y bordes redondeados
        container = create_container(content)
        page.add(container)
        page.update()

    def handle_chat(self, e):
        self.on_chat_selected(e)

    async def handle_practice(self, e):
        await self.on_practice_selected(e)

    def handle_progress(self, e):
        self.on_progress_selected(e)

    def handle_educational_resources(self, e):
        self.on_educational_resources_selected(e)

    async def handle_logout(self, e):
        await self.on_logout(e)