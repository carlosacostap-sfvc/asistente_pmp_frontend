import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime
from src.models.question import Question, Option
from src.models.quiz_session import QuizSession, PracticeSession
from src.models.user import User
from src.config.settings import settings
import random


class APIService:
    def __init__(self):
        self.base_url = settings.API_URL
        self.timeout = settings.API_TIMEOUT
        self.current_user: Optional[User] = None

    async def signup(self, email: str, password: str) -> tuple[bool, str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/auth/signup",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    return True, ""
                return False, response.json().get("detail", "Error en el registro")
        except Exception as e:
            return False, str(e)

    async def login(self, email: str, password: str) -> tuple[bool, str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/auth/token",
                    data={"username": email, "password": password}
                )

                if response.status_code == 200:
                    data = response.json()
                    # Obtenemos los datos del usuario
                    user_response = await client.get(
                        f"{self.base_url}/auth/me",
                        headers={"Authorization": f"Bearer {data['access_token']}"}
                    )
                    user_data = user_response.json()

                    self.current_user = User(
                        email=email,
                        id=user_data["id"],
                        access_token=data["access_token"],
                        is_authenticated=True
                    )
                    return True, ""
                return False, response.json().get("detail", "Error en el login")
        except Exception as e:
            return False, str(e)

    async def get_current_user(self) -> Optional[User]:
        if not self.current_user or not self.current_user.access_token:
            return None

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/auth/me",
                    headers={"Authorization": f"Bearer {self.current_user.access_token}"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return User(
                        email=data["email"],
                        access_token=self.current_user.access_token,
                        is_authenticated=True
                    )
                return None
        except Exception:
            return None

    def logout(self):
        self.current_user = None

    async def get_single_question(self, domain: str) -> Optional[Question]:
        """Obtiene una única pregunta del API."""
        try:
            if domain == "aleatorio":
                domain = random.choice(["personas", "proceso", "entorno"])

            headers = {}
            if self.current_user and self.current_user.access_token:
                headers["Authorization"] = f"Bearer {self.current_user.access_token}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/question",
                    params={"domain": domain},
                    headers=headers
                )
                data = response.json()

                if data.get("data"):
                    return self._parse_question(data["data"])
                return None
        except Exception as e:
            print(f"Error obteniendo pregunta: {e}")
            return None

    async def get_user_practice_sessions(self, user_id: str) -> List[PracticeSession]:
        """Obtiene todas las sesiones de práctica del usuario."""
        try:
            headers = {}
            if self.current_user and self.current_user.access_token:
                headers["Authorization"] = f"Bearer {self.current_user.access_token}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/practice-sessions/user/{user_id}",
                    headers=headers
                )

                if response.status_code == 200:
                    sessions_data = response.json()
                    return [
                        PracticeSession(
                            user_id=session["user_id"],
                            start_time=datetime.fromisoformat(session["start_time"]),
                            end_time=datetime.fromisoformat(session["end_time"]),
                            personas_total=session["personas_total"],
                            personas_correct=session["personas_correct"],
                            proceso_total=session["proceso_total"],
                            proceso_correct=session["proceso_correct"],
                            entorno_total=session["entorno_total"],
                            entorno_correct=session["entorno_correct"],
                            id=session.get("id")
                        )
                        for session in sessions_data
                    ]
                return []
        except Exception as e:
            print(f"Error obteniendo sesiones: {e}")
            return []

    async def save_practice_session(self, session: QuizSession) -> bool:
        """Guarda la sesión de práctica en la base de datos."""
        try:
            if not self.current_user:
                return False

            stats = session.get_stats_by_domain()

            headers = {}
            if self.current_user and self.current_user.access_token:
                headers["Authorization"] = f"Bearer {self.current_user.access_token}"

            session_data = {
                "user_id": self.current_user.id,
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
                    json=session_data,
                    headers=headers
                )

                return response.status_code == 200

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


# Crear instancia global del servicio
api_service = APIService()