from datetime import date
from typing import Protocol


class Relogio(Protocol):
    def hoje(self) -> date: ...