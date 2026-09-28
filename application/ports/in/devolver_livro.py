from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class DevolverLivroComando:
    membro_id: str
    isbn: str


@dataclass(frozen=True)
class DevolucaoRealizada:
    isbn: str
    titulo: str
    multa_aplicada: Decimal
    multa_total_pendente: Decimal


class DevolverLivro(Protocol):
    def executar(self, comando: DevolverLivroComando) -> DevolucaoRealizada: ...