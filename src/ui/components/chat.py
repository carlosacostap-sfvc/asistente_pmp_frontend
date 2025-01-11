import flet as ft
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    user_name: str
    text: str
    message_type: str
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%H:%M")

def create_message_container(message: ChatMessage) -> ft.Container:
    is_user = message.message_type == "user"
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(
                    message.user_name,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_200 if is_user else ft.colors.GREEN_200
                ),
                ft.Text(
                    message.timestamp,
                    size=10,
                    color=ft.colors.GREY_400
                )
            ]),
            ft.Markdown(
                message.text,
                selectable=True,
                code_style=ft.TextStyle(
                    size=14,
                    color=ft.colors.WHITE,
                    font_family="monospace"
                ),
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
            )
        ]),
        bgcolor=ft.colors.BLUE_GREY_900,
        border_radius=10,
        padding=10,
        margin=ft.margin.only(
            left=50 if is_user else 0,
            right=0 if is_user else 50
        )
    )