import flet as ft

def create_title(text: str, size: int = 32, color: str = ft.colors.BLUE_GREY_900) -> ft.Text:
    """Crea un título con el estilo estándar de la aplicación."""
    return ft.Text(
        value=text,
        size=size,
        weight=ft.FontWeight.BOLD,
        color=color,
    )

def create_button(
        text: str,
        on_click=None,
        width: int = 200,
        disabled: bool = False,
        bgcolor: str = None,
        color: str = None,
) -> ft.ElevatedButton:
    """Crea un botón con el estilo estándar de la aplicación."""
    if disabled:
        # Incluso cuando está deshabilitado, mantenemos un color visible pero más suave
        bgcolor = ft.colors.BLUE_200
        color = ft.colors.WHITE
    else:
        bgcolor = bgcolor or ft.colors.BLUE
        color = color or ft.colors.WHITE

    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        width=width,
        disabled=disabled,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=bgcolor,
            color=color,
            overlay_color=ft.colors.TRANSPARENT if disabled else None,
        ),
    )

def create_container(content: ft.Control, padding: int = 50) -> ft.Container:
    """Crea un contenedor con el estilo estándar de la aplicación."""
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLACK12,
        ),
    )

def show_loading(page: ft.Page):
    """Muestra un overlay de carga sobre toda la página."""
    loading_overlay = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.colors.BLACK,
                opacity=0.3,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ProgressRing(
                            width=40,
                            height=40,
                            stroke_width=3,
                            color=ft.colors.BLUE,
                        ),
                        ft.Container(height=20),  # Espaciado
                        ft.Text(
                            "Cargando...",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.WHITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        expand=True,
    )

    if hasattr(page, 'loading_overlay'):
        page.controls.remove(page.loading_overlay)
    page.loading_overlay = loading_overlay
    page.overlay.append(loading_overlay)
    page.update()

def hide_loading(page: ft.Page):
    """Oculta el overlay de carga."""
    if hasattr(page, 'loading_overlay'):
        page.overlay.remove(page.loading_overlay)
        delattr(page, 'loading_overlay')
        page.update()

def show_error_message(page: ft.Page, message: str):
    """Muestra un mensaje de error."""
    error_banner = ft.Banner(
        bgcolor=ft.colors.RED_100,
        leading=ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40),
        content=ft.Text(message, color=ft.colors.RED_900),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: hide_error_message(page))
        ]
    )
    page.show_banner(error_banner)

def hide_error_message(page: ft.Page):
    """Oculta el mensaje de error."""
    if page.banner:
        page.banner.open = False
        page.update()