from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class EmprestarLivroComando:
    membro_id: str
    isbn: str


@dataclass(frozen=True)
class EmprestimoRealizado:
    emprestimo_id: str
    isbn: str
    titulo: str
    data_limite: date


class EmprestarLivro(Protocol):
    def executar(self, comando: EmprestarLivroComando) -> EmprestimoRealizado: ...