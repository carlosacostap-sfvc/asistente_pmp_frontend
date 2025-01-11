import httpx
import logging
from typing import Optional, List
from src.services.api_service import api_service
from src.config.settings import settings

logger = logging.getLogger(__name__)


class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class ChatService:
    def __init__(self):
        self.api_service = api_service
        self.API_URL = f"{settings.API_URL}/chat/"
        self.max_retries = 3
        self.timeout = settings.API_TIMEOUT
        self.message_history: List[ChatMessage] = []

    async def send_message(self, message: str) -> Optional[str]:
        if not self.api_service.current_user:
            return "Error: No has iniciado sesión"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("Enviando mensaje al API")

                # Estructura la solicitud con el historial
                data = {
                    "message": message,
                    "message_history": [
                        {"role": msg.role, "content": msg.content}
                        for msg in self.message_history
                    ],
                    "max_tokens": 4096,
                    "temperature": 0.7
                }

                response = await client.post(
                    self.API_URL,
                    json=data,
                    headers={
                        "Authorization": f"Bearer {self.api_service.current_user.access_token}",
                        "Content-Type": "application/json"
                    }
                )

                if response.status_code == 401:
                    return "Error: Sesión expirada. Por favor, inicia sesión nuevamente."
                elif response.status_code == 404:
                    return "Error: El servicio de chat no está disponible."
                elif response.status_code == 422:
                    logger.error(f"Error de validación: {response.text}")
                    return "Error: Los datos enviados no son válidos."

                response.raise_for_status()
                data = response.json()

                # Actualizar el historial
                self.message_history.append(ChatMessage("user", message))
                self.message_history.append(ChatMessage("assistant", data["response"]))

                return data["response"]

        except httpx.TimeoutException:
            logger.error("Timeout en la solicitud")
            return "Error: El servidor tardó demasiado en responder."

        except Exception as e:
            logger.error(f"Error al enviar mensaje: {str(e)}")
            return f"Error: {str(e)}"

    def clear_history(self):
        """Limpia el historial de mensajes"""
        self.message_history = []


chat_service = ChatService()