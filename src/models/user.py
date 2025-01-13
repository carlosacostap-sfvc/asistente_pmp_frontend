from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    id: str  # Agregamos el campo id
    access_token: Optional[str] = None
    is_authenticated: bool = False