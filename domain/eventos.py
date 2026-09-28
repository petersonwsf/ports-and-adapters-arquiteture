from dataclasses import dataclass
from datetime import date

from domain.value_objects import Isbn


@dataclass(frozen=True)
class LivroEmprestado:
    membro_id: str
    isbn: Isbn
    titulo: str
    data_limite: date