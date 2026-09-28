from dataclasses import dataclass
from datetime import date
from uuid import uuid4

from domain.erros import EmprestimoJaDevolvido
from domain.value_objects import Isbn, PeriodoDeEmprestimo


@dataclass
class Emprestimo:
    id: str
    isbn: Isbn
    membro_id: str
    periodo: PeriodoDeEmprestimo
    devolvido_em: date | None = None

    @classmethod
    def iniciar(cls, isbn: Isbn, membro_id: str, hoje: date) -> "Emprestimo":
        return cls(uuid4().hex, isbn, membro_id, PeriodoDeEmprestimo(hoje))

    @property
    def ativo(self) -> bool:
        return self.devolvido_em is None

    def devolver(self, em: date) -> None:
        if not self.ativo:
            raise EmprestimoJaDevolvido(self.id)
        self.devolvido_em = em