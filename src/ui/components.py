import flet as ft


def create_title(text: str, size: int = 32) -> ft.Text:
    """Crea un título con el estilo estándar de la aplicación."""
    return ft.Text(
        value=text,
        size=size,
        weight=ft.FontWeight.BOLD,
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
        bgcolor = ft.colors.GREY_400
        color = ft.colors.GREY_200

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
    """Muestra un indicador de carga en la parte superior."""
    loading_banner = ft.Container(
        content=ft.Row(
            controls=[
                ft.ProgressRing(
                    width=12,
                    height=12,
                    stroke_width=2,
                    color=ft.colors.BLUE,
                ),
                ft.Text(
                    "Cargando...",
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color=ft.colors.BLUE_GREY_900,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            tight=True,
        ),
        bgcolor=ft.colors.BLUE_50,
        padding=ft.padding.only(left=16, right=16, top=8, bottom=8),
        border_radius=4,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
    )

    # Asegurarnos de que no haya otro banner de carga
    if hasattr(page, 'loading_banner'):
        page.controls.remove(page.loading_banner)
    page.loading_banner = loading_banner

    # Insertar el banner al inicio de los controles
    page.controls.insert(0, loading_banner)
    page.update()


def hide_loading(page: ft.Page):
    """Oculta el indicador de carga."""
    if hasattr(page, 'loading_banner'):
        page.controls.remove(page.loading_banner)
        delattr(page, 'loading_banner')
        page.update()


def show_error_message(page: ft.Page, message: str):
    """Muestra un mensaje de error en la página."""
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