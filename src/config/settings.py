from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    API_URL: str = os.getenv('API_URL', 'http://localhost:8000/api')
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '30'))
    MAX_QUESTIONS: int = int(os.getenv('MAX_QUESTIONS', '100'))

settings = Settings()