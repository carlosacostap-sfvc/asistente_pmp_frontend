from dataclasses import dataclass
from typing import List

@dataclass
class Option:
    text: str
    is_correct: bool

@dataclass
class Question:
    question_text: str
    options: List[Option]
    explanation: str
    domain: str  # Agregamos el atributo domain