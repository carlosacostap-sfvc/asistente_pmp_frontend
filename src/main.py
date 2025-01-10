import os
import sys
import asyncio
from pathlib import Path

# Agregar el directorio raíz al path de Python
root_path = str(Path(__file__).parent.parent)
sys.path.insert(0, root_path)

import flet as ft
from src.app.pmp_quiz_app import PMPQuizApp

async def main():
    """Punto de entrada principal de la aplicación."""
    app = PMPQuizApp()
    await ft.app_async(
        target=lambda page: app.show_main_view(page),
        view=ft.AppView.WEB_BROWSER
    )

if __name__ == "__main__":
    asyncio.run(main())