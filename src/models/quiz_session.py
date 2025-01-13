from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class QuizAnswer:
    question_text: str
    selected_option: str
    correct_option: str
    is_correct: bool
    domain: str
    explanation: str


@dataclass
class QuizSession:
    start_time: datetime
    answers: List[QuizAnswer]

    def add_answer(self, answer: QuizAnswer):
        self.answers.append(answer)

    def get_stats_by_domain(self) -> Dict[str, Dict[str, int]]:
        stats = {}
        for answer in self.answers:
            if answer.domain not in stats:
                stats[answer.domain] = {"total": 0, "correct": 0}
            stats[answer.domain]["total"] += 1
            if answer.is_correct:
                stats[answer.domain]["correct"] += 1
        return stats


@dataclass
class PracticeSession:
    user_id: str
    start_time: datetime
    end_time: datetime
    personas_total: int
    personas_correct: int
    proceso_total: int
    proceso_correct: int
    entorno_total: int
    entorno_correct: int
    id: int = None