from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    access_token: Optional[str] = None
    is_authenticated: bool = False