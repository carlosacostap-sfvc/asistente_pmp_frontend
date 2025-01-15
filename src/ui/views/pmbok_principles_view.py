import flet as ft
from typing import Callable
from src.ui.components import create_title, create_container, create_button


class PMBOKPrinciplesView:
    def __init__(self, on_return_to_resources: Callable):
        self.on_return_to_resources = on_return_to_resources
        self.page = None

    def create_principle_card(self, number: int, title: str, description: str) -> ft.Container:
        def handle_card_click(e):
            from src.ui.views.principle_chat_view import PrincipleChatView
            chat_view = PrincipleChatView(
                principle_number=number,
                title=title,
                description=description,
                on_return_to_principles=lambda e: self.build(self.page)
            )
            chat_view.build(self.page)

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(str(number),
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE,
                        radius=15,
                    ),
                    ft.Text(
                        title,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                    )
                ], alignment=ft.MainAxisAlignment.START, spacing=10),
                ft.Text(
                    description,
                    size=14,
                    color=ft.colors.BLACK,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ]),
            padding=20,
            margin=ft.margin.only(bottom=10),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLUE_200),
            on_click=handle_card_click,
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
            # Agregamos un hover effect usando el property scale
            scale=ft.transform.Scale(scale=1),
            animate_scale=300,
            on_hover=lambda e: self.handle_card_hover(e),
        )

    def handle_card_hover(self, e):
        """Maneja el efecto hover de las tarjetas"""
        e.control.scale = ft.transform.Scale(scale=1.02) if e.data == "true" else ft.transform.Scale(scale=1)
        e.control.update()

    def handle_principle_click(self, principle_data: dict):
        """Maneja el click en un principio específico"""
        from src.ui.views.management_principles_view import PrincipleDetailView
        detail_view = PrincipleDetailView(
            principle=principle_data,
            on_return_to_principles=lambda e: self.build(self.page)
        )
        detail_view.build(self.page)

    def build(self, page: ft.Page):
        self.page = page
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 40
        page.spacing = 20

        principles = [
            ("Sea un administrador diligente, respetuoso y cuidadoso",
             "Demuestra compromiso con el bienestar de las personas, el medio ambiente y los resultados del proyecto."),

            ("Cree un entorno colaborativo del equipo del proyecto",
             "Fomenta un ambiente de trabajo positivo, inclusivo y psicológicamente seguro que promueva la colaboración efectiva."),

            ("Involucre efectivamente a los interesados",
             "Comprende, involucra y gestiona las expectativas de todos los interesados del proyecto de manera proactiva."),

            ("Enfóquese en el valor",
             "Mantén el foco en entregar valor al negocio y los beneficios esperados del proyecto."),

            ("Reconozca, evalúe y responda a las interacciones del sistema",
             "Visualiza el proyecto como un sistema complejo y gestiona las interdependencias entre componentes."),

            ("Demuestre comportamiento de liderazgo",
             "Inspira, influye y guía al equipo y los interesados hacia resultados exitosos."),

            ("Adapte según el contexto",
             "Ajusta el enfoque del proyecto basado en el contexto, las restricciones y las condiciones."),

            ("Incorpore la calidad en los procesos y entregables",
             "Planifica y ejecuta con un enfoque en la calidad en todos los aspectos del proyecto."),

            ("Navegue en la complejidad",
             "Reconoce y adapta las estrategias para manejar la complejidad inherente del proyecto."),

            ("Optimice las respuestas a los riesgos",
             "Identifica y gestiona proactivamente las amenazas y oportunidades del proyecto."),

            ("Adopte la adaptabilidad y la resiliencia",
             "Se adapta a los cambios y mantiene la efectividad frente a la incertidumbre."),

            ("Permita el cambio para lograr el estado futuro previsto",
             "Reconoce y facilita los cambios necesarios para alcanzar los objetivos del proyecto.")
        ]

        # Contenido principal
        content = ft.Column([
            create_title("Los 12 Principios del PMBOK 7"),

            ft.Text(
                "El PMBOK 7 se centra en 12 principios fundamentales que guían la gestión efectiva de proyectos:",
                size=16,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_500
            ),

            # Contenedor para las tarjetas de principios
            ft.Container(
                content=ft.Column([
                    self.create_principle_card(i + 1, title, desc)
                    for i, (title, desc) in enumerate(principles)
                ], spacing=10),
                padding=ft.padding.only(top=20, bottom=20)
            ),

            # Botón de retorno
            create_button(
                text="Volver a Recursos",
                on_click=self.on_return_to_resources,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            )
        ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # Contenedor principal con sombra y bordes redondeados
        main_container = ft.Container(
            content=content,
            width=float("inf"),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=40,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

        page.add(main_container)
        page.update()