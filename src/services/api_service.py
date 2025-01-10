import httpx
from typing import Optional, Dict, Any
from datetime import datetime
from src.models.question import Question, Option
from src.models.quiz_session import QuizSession
from src.config.settings import settings


class APIService:
    def __init__(self):
        self.base_url = settings.API_URL
        self.timeout = settings.API_TIMEOUT

    async def get_single_question(self, domain: str) -> Optional[Question]:
        """Obtiene una única pregunta del API."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/question",
                    params={"domain": domain}
                )
                data = response.json()

                if data["success"] and data["data"]:
                    return self._parse_question(data["data"])
                return None
        except Exception as e:
            print(f"Error obteniendo pregunta: {e}")
            return None

    async def save_practice_session(self, session: QuizSession) -> bool:
        """Guarda la sesión de práctica en la base de datos."""
        try:
            # Obtener estadísticas por dominio
            stats = session.get_stats_by_domain()

            # Preparar datos para enviar al API
            session_data = {
                "start_time": session.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "personas_total": stats.get("personas", {}).get("total", 0),
                "personas_correct": stats.get("personas", {}).get("correct", 0),
                "proceso_total": stats.get("proceso", {}).get("total", 0),
                "proceso_correct": stats.get("proceso", {}).get("correct", 0),
                "entorno_total": stats.get("entorno", {}).get("total", 0),
                "entorno_correct": stats.get("entorno", {}).get("correct", 0)
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/practice-sessions",
                    json=session_data
                )

                if response.status_code == 200:
                    return True
                return False

        except Exception as e:
            print(f"Error guardando la sesión: {e}")
            return False

    def _parse_question(self, question_data: Dict[str, Any]) -> Question:
        """Convierte los datos JSON de una pregunta en un objeto Question."""
        return Question(
            question_text=question_data["question_text"],
            options=[Option(**opt) for opt in question_data["options"]],
            explanation=question_data["explanation"],
            domain=question_data["domain"]
        )


api_service = APIService()